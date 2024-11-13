# Telegram Channel Cloner Bot

This is a Telegram bot that forwards messages from a source channel to a destination channel using the Telethon library. The bot is designed to support a large number of messages, track progress, and handle interruptions by saving the last forwarded message.

## Features

- Fetches all messages from a source Telegram channel.
- Forwards messages to a destination channel.
- Tracks forwarding progress and supports resuming from the last forwarded message.
- Allows customizable cooldown period between forwarding actions.

## Prerequisites

- Python 3.7+
- A Telegram account and API credentials (API ID, API Hash).
- Source and Destination Channel IDs.

## Setup

1. Clone this repository.
   ```bash
   git clone https://github.com/yourusername/telegram-forward-bot.git
   cd telegram-forward-bot
   ```

2. Install dependencies.
   ```bash
   pip install -r requirements.txt
   ```

3. Edit the `.env` file with your API credentials and channel information.
   ```plaintext
   API_ID=YOUR_API_ID
   API_HASH=YOUR_API_HASH
   PHONE_NUMBER=YOUR_PHONE_NUMBER
   SOURCE_CHANNEL=SOURCE_CHANNEL_ID
   DESTINATION_CHANNEL=DESTINATION_CHANNEL_ID
   ```

## Running the Bot

Run the bot with:
```bash
python main.py
```

The bot will automatically fetch messages from the source channel and forward them to the destination channel with progress tracking. If interrupted, it will resume from the last forwarded message.

## Configuration

- **Cooldown:** Adjust the `COOLDOWN` variable in `main.py` to set the delay (in seconds) between each message forward action.

