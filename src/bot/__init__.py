from telegram.ext import Application, CommandHandler, MessageHandler, filters

from src.config import TELEGRAM_TOKEN, ALLOWED_USER_IDS
from src.bot.commands.message import message
from src.bot.commands.recipe import recipe
from src.bot.commands.inventory import inventory
from src.bot.commands.expiring import expiring

# only allowed users reach the handlers, everyone else is ignored
allowed = filters.User(user_id=ALLOWED_USER_IDS)

def run ():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("receta", recipe, filters=allowed))
    app.add_handler(CommandHandler("inventario", inventory, filters=allowed))
    app.add_handler(CommandHandler("caduca", expiring, filters=allowed))
    app.add_handler(MessageHandler(allowed & filters.TEXT & ~filters.COMMAND, message))
    app.run_polling()
