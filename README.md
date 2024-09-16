# WarrantyAndStockBot--Discord
This bot is designed to handle customer support tasks on Discord, including warranty claims, stock management, and providing information about payment methods and premium app terms.

## Features

- **Warranty Claims**: Users can claim warranties for various apps using specific commands and formats.
- **Stock Management**: Admins can manage stock for products with commands to add or remove stock.
- **Payment Information**: Users can view accepted payment methods.
- **Premium App Terms**: Users can view terms and conditions for premium apps.
- **AFK Status**: Users can set their AFK status, which will be announced when they are mentioned.
- **Command List**: Includes various commands for stock checking, payment information, and more.

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/discord-support-bot.git
    cd discord-support-bot
    ```

2. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `config.json` file with the following structure:
    ```json
    {
        "prefix": "!",
        "bot_name": "YourBotName",
        "token": "YOUR_BOT_TOKEN",
        "report_channel_id": "YOUR_REPORT_CHANNEL_ID",
        "buyer_roles": ["ROLE_ID_1", "ROLE_ID_2"],
        "admin_roles": ["ADMIN_ROLE_ID_1", "ADMIN_ROLE_ID_2"]
    }
    ```

5. Create a `stock.json` file with initial stock data:
    ```json
    {
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
    }
    ```

6. Run the bot:
    ```bash
    python bot.py
    ```

## Commands

- **Warranty Claims**:
  - `.canvagaransi`: Claim warranty for Canva.
  - `.netflixgaransi`: Claim warranty for Netflix.
  - `.spotifygaransi`: Claim warranty for Spotify.
  - `.otherapp`: Claim warranty for other applications.

- **User Commands**:
  - `.help`: Displays all available commands.
  - `.stok [appname]`: Check stock for a specific app or all apps.
  - `.payment`: Displays accepted payment methods.
  - `.snkappprem`: Shows terms and conditions for premium apps.

- **Admin Commands**:
  - `.addproduk [product_name] [quantity]`: Add a new product or update stock.
  - `.removeproduk [product_name]`: Remove a product from the list.
  - `.removestok [app] [quantity]`: Remove stock for a specific app.
  - `.addstok [app] [quantity]`: Add stock for a specific app.
  - `.afk [status] [reason]`: Set or remove AFK status.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
