from telegram import Update
from telegram.ext import ContextTypes

from src.bot.format import item_line
from src.db import inventory as db

# /caduca [days] lists what expires in the next days (3 by default), including what is already expired
async def expiring (update: Update, context: ContextTypes.DEFAULT_TYPE):
    days = int(context.args[0]) if context.args and context.args[0].isdigit() else 3
    rows = db.expiring_soon(update.effective_user.id, days)

    if not rows:
        await update.message.reply_text(f"No caduca nada en los próximos {days} días.")
        return

    await update.message.reply_text("\n".join(item_line(r) for r in rows))
