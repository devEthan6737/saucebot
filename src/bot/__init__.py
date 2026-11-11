from telegram.ext import Application, MessageHandler, filters

from src.config import TELEGRAM_TOKEN, ALLOWED_USER_IDS
from src.bot.commands.message import message

# only allowed users reach the handlers, everyone else is ignored
allowed = filters.User(user_id=ALLOWED_USER_IDS)

def run ():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(allowed & filters.TEXT & ~filters.COMMAND, message))
    app.run_polling()
