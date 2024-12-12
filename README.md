Here's a sample **README.md** for your Telegram Proxy Bot script with installation instructions in English:

```markdown
# Telegram Proxy Bot

This is a Python script that interacts with Telegram via the `python-telegram-bot` library. It fetches proxies from one Telegram channel, tests them, and sends the working proxies to another Telegram channel.

## Requirements

- Python 3.9 or later
- `python-telegram-bot` library
- `requests` library (if necessary for testing proxies)

## Installation

Follow these steps to install and run the bot on your local machine or server:

### 1. Clone the repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/your-username/repository-name.git
cd repository-name
```

### 2. Set up a virtual environment (optional but recommended)

It's recommended to use a virtual environment to manage dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install dependencies

Install the required Python packages by running:

```bash
pip install -r requirements.txt
```

If you don't have the `requirements.txt` file, you can manually install the dependencies:

```bash
pip install python-telegram-bot requests
```

### 4. Set up your Telegram Bot

1. Create a new bot on Telegram by chatting with the [BotFather](https://core.telegram.org/bots#botfather) and following the instructions.
2. Copy the bot token provided by BotFather.

### 5. Set up environment variables

Create a `.env` file (or use GitHub Secrets if deploying to GitHub Actions) to store your bot token:

```bash
TELEGRAM_BOT_TOKEN=your-bot-token-here
```

### 6. Run the bot

After setting up the bot token, you can run the script using:

```bash
python proxy_bot.py
```

The bot will start listening for messages, fetch proxies from the source channel, test them, and send the working ones to the destination channel.

## Troubleshooting

- **Issue: ImportError: cannot import name 'Filters' from 'telegram.ext'**
  - This issue arises because the `Filters` module was replaced with `filters` in recent versions of `python-telegram-bot` (v20+).
  - **Solution:** Use `filters` instead of `Filters` as shown below:

    ```python
    from telegram.ext import Application, CommandHandler, MessageHandler, filters
    ```

- **Issue: File not found error**
  - Ensure that the path to the Python script is correct. If your script is in a subfolder, use the correct relative path.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### Key Details in the README:
- **Requirements:** This section lists the required libraries and Python version.
- **Installation Instructions:** Detailed steps on cloning the repository, setting up a virtual environment, installing dependencies, and setting up the bot.
- **Bot Setup:** Steps for obtaining the Telegram bot token and using it in the script.
- **Running the Bot:** Instructions to run the bot with the correct command.
- **Troubleshooting:** Helpful information to solve common issues, like the `ImportError` with the `filters` module.

This README will help users set up and run your bot efficiently.
