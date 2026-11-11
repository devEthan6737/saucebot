# saucebot

A Telegram bot that keeps track of what you have in your kitchen, suggests recipes and teaches you how to cook them live, by voice.

Built with Python, LangChain, DeepSeek, SQLite, vosk and Piper.

## Features

- Per-user inventory with quantity, unit and optional expiry date
- Alerts for products that expire soon
- Recipe suggestions based on your inventory
- Voice notes in Telegram
- Live chef: a web page where you talk with the chef while you cook the recipe
- Access limited to allowed Telegram users

## Telegram commands

- `/inventario` lists everything you have
- `/caduca [days]` lists what expires soon
- `/receta [preferences]` designs a recipe with your products
- `/compra` shows the shopping list: products at or below the minimum you want to have

You can also write or send a voice note in plain language, for example "I bought two litres of milk".

## Status

Work in progress.

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
PUBLIC_URL=https://chef.yourdomain.com
```

`PUBLIC_URL` is the address of the live chef web, it is the base of the links sent to Telegram. The default is `http://localhost:8000`. Optional: `WEB_HOST`, `WEB_PORT`, `VOSK_MODEL_PATH`, `PIPER_VOICE_PATH`.

Voice models, in the `models/` folder (not in git):

- [vosk-model-small-es-0.42](https://alphacephei.com/vosk/models) in `models/vosk-model-small-es-0.42`
- [es_ES-davefx-medium](https://huggingface.co/rhasspy/piper-voices/tree/main/es/es_ES/davefx/medium) (`.onnx` and `.onnx.json`) in `models/piper/`

`ffmpeg` is needed to transcribe Telegram voice notes.

## Run

One command starts the bot and the live chef web together:

```bash
python -m src.bot
```

The web can also run alone with `python -m src.web`.

The microphone only works on `localhost` or with HTTPS, so to use the live chef from your phone the web needs a domain with HTTPS.

## Project structure

```
src/
├── config.py        # loads .env
├── db/              # sqlite connection, inventory, cooking sessions and sql queries
├── agent/           # telegram agent: model, personality, memory and tools
├── chef/            # live chef agent
├── voice/           # speech to text (vosk) and text to speech (piper)
├── bot/             # telegram bot and commands
└── web/             # live chef web server and page
```
