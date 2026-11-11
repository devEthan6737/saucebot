# saucebot

A Telegram bot that keeps track of what you have in your kitchen, suggests recipes and builds your shopping list.

Built with Python, LangChain, DeepSeek and SQLite.

## Features

- Per-user inventory with quantity, unit and optional expiry date
- Alerts for products that expire soon
- Recipe suggestions based on your inventory
- Shopping list
- Access limited to allowed Telegram users

## Status

Work in progress. The inventory database layer is done; the Telegram bot, the LangChain agent and the shopping list are still pending.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```
TELEGRAM_TOKEN=your-bot-token
DEEPSEEK_API_KEY=sk-....
ALLOWED_USER_IDS=123456789,987654321
```

## Project structure

```
src/
├── config.py        # loads .env
└── db/
    ├── __init__.py  # sqlite connection and sql helpers
    ├── inventory.py # inventory functions
    └── sql/         # sql queries
```
