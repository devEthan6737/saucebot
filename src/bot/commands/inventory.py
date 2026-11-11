from telegram import Update
from telegram.ext import ContextTypes

from src.bot.format import item_line
from src.db import inventory as db

# /inventario lists everything the user has
async def inventory (update: Update, context: ContextTypes.DEFAULT_TYPE):
    rows = db.list_items(update.effective_user.id)

    if not rows:
        await update.message.reply_text("Tu inventario está vacío.")
        return

    await update.message.reply_text("\n".join(item_line(r) for r in rows))
