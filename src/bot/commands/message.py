from telegram import Update
from telegram.ext import ContextTypes

from src.agent import ask

# handles any text message from an allowed user
async def message (update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = await ask(update.effective_user.id, update.message.text)
    await update.message.reply_text(answer)
