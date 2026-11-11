from telegram.ext import Application, CommandHandler, MessageHandler, filters

from src import web
from src.config import TELEGRAM_TOKEN, ALLOWED_USER_IDS
from src.bot.commands.message import message
from src.bot.commands.recipe import recipe
from src.bot.commands.inventory import inventory
from src.bot.commands.expiring import expiring
from src.bot.commands.shopping import shopping
from src.bot.commands.voice import voice

# only allowed users reach the handlers, everyone else is ignored
allowed = filters.User(user_id=ALLOWED_USER_IDS)

def run ():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("receta", recipe, filters=allowed))
    app.add_handler(CommandHandler("inventario", inventory, filters=allowed))
    app.add_handler(CommandHandler("caduca", expiring, filters=allowed))
    app.add_handler(CommandHandler("compra", shopping, filters=allowed))
    app.add_handler(MessageHandler(allowed & filters.VOICE, voice))
    app.add_handler(MessageHandler(allowed & filters.TEXT & ~filters.COMMAND, message))

    # the live chef web starts together with the bot
    server = web.start()
    try:
        app.run_polling()
    finally:
        server.should_exit = True
