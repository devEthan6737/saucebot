import asyncio
import tempfile
from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

from src.agent import ask
from src.voice import stt

# a voice note is transcribed and then handled like any text message
async def voice (update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not stt.model_exists():
        await update.message.reply_text("Falta el modelo de voz, no puedo transcribir notas de voz todavía.")
        return

    file = await update.message.voice.get_file()

    with tempfile.TemporaryDirectory() as folder:
        ogg = Path(folder) / "voice.ogg"
        await file.download_to_drive(ogg)
        text = await asyncio.to_thread(stt.transcribe, ogg)

    if not text:
        await update.message.reply_text("No te he entendido, repítelo.")
        return

    # show what was understood, so mistakes in the transcription are easy to spot
    await update.message.reply_text(f"Entendí: {text}")
    await update.message.reply_text(await ask(update.effective_user.id, text))
