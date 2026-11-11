from telegram import Update
from telegram.ext import ContextTypes

from src.db import inventory as db

# /compra lists what is at or below the minimum the user wants to have
async def shopping (update: Update, context: ContextTypes.DEFAULT_TYPE):
    rows = db.low_stock(update.effective_user.id)

    if not rows:
        await update.message.reply_text("No te falta nada. Si quieres una lista, dime qué cantidad mínima quieres tener de cada cosa.")
        return

    lines = [
        f"- {r['productName']}: tienes {r['productQuantity']:g} {r['productUnit']} (mínimo {r['productMinQuantity']:g})"
        for r in rows
    ]
    await update.message.reply_text("Lista de la compra:\n" + "\n".join(lines))
