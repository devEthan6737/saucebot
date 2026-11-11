import asyncio

from telegram import Update
from telegram.ext import ContextTypes

from src.agent.recipes import generate_recipe

def _lines (ingredients):
    return "\n".join(f"- {i.name}: {i.quantity:g} {i.unit}" for i in ingredients) or "- nada"

# /receta [preferences] designs a recipe from the inventory, without going through the agent
async def recipe (update: Update, context: ContextTypes.DEFAULT_TYPE):
    preferences = " ".join(context.args) or None

    # the model call is blocking, run it outside the event loop
    result = await asyncio.to_thread(generate_recipe, update.effective_user.id, preferences)

    if result is None:
        await update.message.reply_text("Tu inventario está vacío, no hay nada con lo que cocinar.")
        return

    await update.message.reply_text(
        f"{result.name}\n{result.description}\nRaciones: {result.servings}\n\n"
        f"Lo que tienes:\n{_lines(result.in_stock)}\n\n"
        f"Lo que te falta:\n{_lines(result.missing)}"
    )
