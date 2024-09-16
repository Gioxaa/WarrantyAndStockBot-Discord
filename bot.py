import discord
from discord.ext import commands
import asyncio
import json
import os
import datetime
import random

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

# Load stock data
def load_stock():
    if not os.path.exists('stock.json'):
        with open('stock.json', 'w') as file:
            json.dump({
                "netflix": 0,
                "canva": 0,
                "youtube": 0,
                "vidio": 0,
                "iqiyi": 0,
                "capcut": 0,
                "amazon-prime-video": 0,
                "we-tv": 0,
                "bstation": 0,
                "spotify": 0,
                "get-contact": 0,
                "zoom-meeting": 0
            }, file)
    with open('stock.json') as file:
        return json.load(file)

def save_stock(stock):
    with open('stock.json', 'w') as file:
        json.dump(stock, file, indent=4)



afk_status = {}
def is_afk(user_id):
    return user_id in afk_status

def is_afk(user_id):
    return user_id in afk_status

# Bot setup with intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config['prefix'], intents=intents)
bot.remove_command('help')

def has_buyer_role(ctx):
    user_roles = [role.id for role in ctx.author.roles]
    return any(role_id in user_roles for role_id in config['buyer_roles'])

def is_admin(ctx):
    user_roles = [role.id for role in ctx.author.roles]
    return any(role_id in user_roles for role_id in config['admin_roles'])

def get_current_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

async def handle_warranty(ctx, format_name, expected_format):
    if not has_buyer_role(ctx):
        await ctx.send("Anda tidak memiliki izin untuk menggunakan command ini.")
        return

    await ctx.send(f"{expected_format}\n\n**WAJIB MENGGUNAKAN FORMAT INI**\nKetik 'cancel' untuk membatalkan proses.")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    while True:
        try:
            msg = await bot.wait_for('message', check=check, timeout=300.0)

            if msg.content.lower() == 'cancel':
                await ctx.send("Proses garansi dibatalkan.")
                print(f"[LOG] {ctx.author.display_name} membatalkan proses garansi {format_name}.")
                return  # Exit the function to end the process

            if format_name in msg.content.upper():
                confirm_message = await ctx.send("Apakah format sudah benar? Silakan konfirmasi.")
                await confirm_message.add_reaction('✅')
                await confirm_message.add_reaction('❌')

                def confirm_check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ['✅', '❌'] and reaction.message == confirm_message

                try:
                    reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=confirm_check)

                    if str(reaction.emoji) == '✅':
                        report_channel = bot.get_channel(config['report_channel_id'])
                        await report_channel.send(f"<@939756275561025577>\n# GARANSI {format_name.upper()}\nUser: <@{user.id}>\n```{msg.content}```")
                        await ctx.send("Support akan membantu segera!")
                        print(f"[LOG] {ctx.author.display_name} Ingin Claim Garansi {format_name}, Cek Server!")
                    else:
                        await ctx.send("Silakan perbaiki format dan kirim ulang.")
                        continue

                except asyncio.TimeoutError:
                    await ctx.send("Waktu konfirmasi habis. Silakan ulangi proses.")
                
                break
            else:
                await ctx.send(f"Format salah. Harap gunakan format yang benar: {expected_format}")

        except discord.TimeoutError:
            await ctx.send("Waktu habis. Silakan ulangi command ini jika Anda ingin claim garansi.")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Melayani Customer"))
    clear()
    print(f"{config['bot_name']} is online!")
    os.system("title SUPPORT BOT BY GIOXA")

# Command: .start
@bot.command()
async def start(ctx):
    if has_buyer_role(ctx):
        embed = discord.Embed(
            title="🏆 **GARANSI COMMAND**",
            # description="Silakan pilih kategori produk yang sesuai dan gunakan command yang tersedia:",
            color=discord.Color.from_rgb(255, 223, 0)
        )
        
        # Adding fields to the embed
        embed.add_field(
            name="",
            value=(
                "Silakan pilih kategori produk yang sesuai dan gunakan command yang tersedia:\n\n"
                "**.canvagaransi** - Claim garansi untuk Canva\n"
                "**.netflixgaransi** - Claim garansi untuk Netflix\n"
                "**.spotifygaransi** - Claim garansi untuk Spotify\n"
                "**.otherapp** - Claim garansi untuk aplikasi lainnya"
            ),
            inline=False
        )

        # Adding an image to the embed
        embed.set_image(url="https://message.style/cdn/images/ba4c3c8870e2812c94ab6a3768de7aa519d74adb38c70fa027e8c4ec85e2b1de.gif")  # Replace with your image URL

        # Sending the embed
        await ctx.send(embed=embed)
    else:
        await ctx.send("Anda tidak memiliki izin untuk menggunakan command ini.")



# Command handlers for each warranty type
@bot.command()
async def canvagaransi(ctx):
    await handle_warranty(ctx, "CANVA", "FORMAT CANVA\n\nEmail: \nDesainer/Member: \nDurasi Order: ")

@bot.command()
async def netflixgaransi(ctx):
    await handle_warranty(ctx, "NETFLIX", "FORMAT NETFLIX\nEmail: ")

@bot.command()
async def spotifygaransi(ctx):
    await handle_warranty(ctx, "SPOTIFY", "FORMAT SPOTIFY\nEmail: ")

@bot.command()
async def otherapp(ctx):
    await handle_warranty(ctx, "APLIKASI LAIN", "FORMAT APLIKASI LAIN\nEmail: ")

# User Commands
@bot.command()
async def help(ctx):  
    embed = discord.Embed(
            title=":clipboard: **Help Command**",
            description=(
                "Berikut adalah daftar command yang tersedia:\n"
                ".help - Menampilkan semua command\n"
                ".stok - Mengecek stok seluruh barang\n"
                ".stok (appname) - Mengecek stok untuk aplikasi tertentu\n"
                ".payment - Menampilkan metode pembayaran yang diterima\n"
                ".snkappprem - Menampilkan syarat dan ketentuan aplikasi premium\n"
                ".payment - Menampilkan Payment apa saja yang di terima oleh Seller\n"
                
            ),
            color=discord.Color.from_rgb(255, 223, 0)
        )
    embed.add_field(
            name="**Admin Command:**",
            value=(
                "\n.addproduk (app) (count) - Menambahkan Sebuah Produk\n"
                ".removeproduk (app) - Menghapus Sebuah Produk\n"
                ".addstok (appname) (amount)\n"
                ".removestock (app) (count) - Menghapus stok untuk aplikasi\n"
                ".afk off (reason)"
                ""
            ),
            inline=False
        )
    embed.set_image(url="https://message.style/cdn/images/ba4c3c8870e2812c94ab6a3768de7aa519d74adb38c70fa027e8c4ec85e2b1de.gif")

        # Sending the embed
    await ctx.send(embed=embed)


@bot.command()
async def stok(ctx, app=None):
    stock = load_stock()
    if app:
        app = app.lower()
        if app in stock:
            await ctx.send(f"Stok untuk {app.capitalize()}: {stock[app]}")
        else:
            await ctx.send("Aplikasi tidak ditemukan.")
    else:
        response = "\n".join([f"{app.capitalize()}: {count}" for app, count in stock.items()])
        embed = discord.Embed(
            title=":clipboard: **STOCK PRODUCT**",
            description=(
                f"{response}"
                
            ),
            color=discord.Color.from_rgb(255, 223, 0)
        )
        await ctx.send(embed=embed)
        

@bot.command()
async def payment(ctx):
    embed = discord.Embed(
            title=":credit_card: **PAYMENT**",
            description=(
                "*Payment Accept:*"
                "```" 
                "> DANA    ┃ 081234567899 a/n yourname\n"
                "```"
            ),
            color=discord.Color.from_rgb(255, 223, 0)
        )
    embed.add_field(
            name="**Note:**",
            value=(
                "- Untuk DANA apabila transfer melalu bank mana pun, wajib nominal transfer nya ditambah Rp500 dari harga awal. \n"
                "> -  Contoh buat transfer yang nominalnya wajib ditambah untuk dana: harga beli nya Rp50.000, tapi lu transfer nya melalui bank, bukan sesama ovo/dana, maka wajib dilebihin menjadi Rp50.500\n"
                "- Kirim Bukti Transfer Jika memesan Produk,\n"
                "- Tidak ada REFFUND jika sudah memesan, dan pesanan akan di proses."
            ),
            inline=False
    )
    await ctx.send(embed=embed)

@bot.command()
async def snkappprem(ctx):
    embed = discord.Embed(title="SYARAT DAN KETENTUAN TIAP APP PREMIUM",
                        description="NETFLIX >> https://discord.com/channels/1259443545417191435/1275476166026854441/1275716314845151233\n\nCANVA >>  https://discord.com/channels/1259443545417191435/1275476166026854441/1275717844817940511\n\nVIDIO >> https://discord.com/channels/1259443545417191435/1275476166026854441/1275718647620304907\n\nIQIYI >> https://discord.com/channels/1259443545417191435/1275476166026854441/1275719262547476480\n\nCAPCUT PRO SHARING >> https://discord.com/channels/1259443545417191435/1275476166026854441/1275720047381188651\n\nAMAZON PRIME VID >> https://discord.com/channels/1259443545417191435/1275476166026854441/1275720691752112170",
                        colour=0x93f500)

    embed.set_image(url="https://message.style/cdn/images/ba4c3c8870e2812c94ab6a3768de7aa519d74adb38c70fa027e8c4ec85e2b1de.gif")

    await ctx.send(embed=embed)
    

@bot.command()
async def addproduk(ctx, produk_name: str, jumlah: int):
    if is_admin(ctx):
        stock = load_stock()
        # Add the product to the list or update if it exists
        if produk_name in stock:
            stock[produk_name] += jumlah
        else:
            stock[produk_name] = jumlah
        save_stock(stock)
        await ctx.send(f"Produk `{produk_name}` berhasil ditambahkan dengan stok {jumlah}.")
        print(f"{produk_name} Telah di tambahkan dengan stok {jumlah}" )
    else:
        await ctx.send("Anda tidak memiliki izin untuk menggunakan command ini.")

@bot.command()
async def removeproduk(ctx, produk_name: str):
    if is_admin(ctx):
        stock = load_stock()
        # Remove the product if it exists
        if produk_name in stock:
            del stock[produk_name]
            save_stock(stock)
            await ctx.send(f"Produk `{produk_name}` berhasil dihapus dari Daftar Produk.")
            print(f"{produk_name} Telah di hapus dari daftar" )
        else:
            await ctx.send(f"Produk `{produk_name}` tidak ditemukan di list stok.")
            print(f"{produk_name} Not Found in List" )
    else:
        await ctx.send("Anda tidak memiliki izin untuk menggunakan command ini.")
        
@bot.command()
async def removestok(ctx, app, count: int):
    if not is_admin(ctx):
        await ctx.send("Anda tidak memiliki izin untuk menggunakan command ini.")
        return
    
    stock = load_stock()
    app = app.lower()
    if app in stock:
        old_amount = stock[app]
        stock[app] = max(0, stock[app] - count)
        save_stock(stock)
        print(f"[LOG] {get_current_time()} - Pengurangan stok: {app.capitalize()} - Jumlah awal: {old_amount} - Jumlah yang dikurangi: {count} - Jumlah sekarang: {stock[app]}")
        await ctx.send(f"Stok untuk {app.capitalize()} telah diubah menjadi {stock[app]}.")
    else:
        await ctx.send("Aplikasi tidak ditemukan.")

@bot.command()
async def addstok(ctx, app, count: int):
    if not is_admin(ctx):
        await ctx.send("Anda tidak memiliki izin untuk menggunakan command ini.")
        return
    
    stock = load_stock()
    app = app.lower()
    if app in stock:
        old_amount = stock[app]
        stock[app] += count
        save_stock(stock)
        print(f"[LOG] {get_current_time()} - Penambahan stok: {app.capitalize()} - Jumlah awal: {old_amount} - Jumlah yang ditambahkan: {count} - Jumlah sekarang: {stock[app]}")
        await ctx.send(f"Stok untuk {app.capitalize()} telah ditambahkan menjadi {stock[app]}.")
    else:
        await ctx.send("Aplikasi tidak ditemukan.")

@bot.command()
async def afk(ctx, status: str, *, reason: str = "AFK"):
    if not is_admin(ctx):
        await ctx.send(f"{ctx.author.mention} Anda tidak memiliki izin untuk menggunakan command ini.")
        return
    
    user_id = ctx.author.id
    current_time = datetime.datetime.now()

    if status.lower() == "off":
        afk_status[user_id] = {"reason": reason, "time": current_time}
        await ctx.send(f"{ctx.author.mention} is now AFK: {reason}")
    else:
        afk_status.pop(user_id, None)
        await ctx.send(f"{ctx.author.mention} is no longer AFK.")

# Event to detect when someone mentions the bot owner
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    current_time = datetime.datetime.now()

    # Check if the bot owner is mentioned
    for user in message.mentions:
        if is_afk(user.id):
            afk_info = afk_status.get(user.id)
            reason = afk_info.get("reason", "AFK")
            await message.channel.send(f"{user.name} sedang afk: {reason}")

    # If the AFK user sends a message, clear their AFK status and calculate AFK time
    if message.author.id in afk_status:
        afk_info = afk_status.pop(message.author.id)
        afk_time = afk_info["time"]
        afk_duration = current_time - afk_time
        hours, remainder = divmod(afk_duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Calculate how long the user has been AFK
        afk_duration_str = f"{hours} jam, {minutes} menit, and {seconds} detik"
        await message.channel.send(f"Welcome back, {message.author.mention}! You were AFK for {afk_duration_str}.")
    # Process commands
    await bot.process_commands(message)


bot.run(config['token'])
