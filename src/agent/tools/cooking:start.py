from langchain.tools import tool, ToolRuntime

from src.agent.context import Context
from src.agent.recipes import Ingredient
from src.config import PUBLIC_URL
from src.db import sessions

@tool
def start_cooking (
    name: str,
    description: str,
    servings: int,
    in_stock: list[Ingredient],
    missing: list[Ingredient],
    runtime: ToolRuntime[Context],
) -> str:
    """Create a live cooking session for a recipe that the user has accepted, copying it exactly as the recipe tool returned it.
    It returns a link to a web page where the chef teaches the user how to cook it by voice. Give the link to the user."""
    recipe = {
        "name": name,
        "description": description,
        "servings": servings,
        "in_stock": [ i.model_dump() for i in in_stock ],
        "missing": [ i.model_dump() for i in missing ],
    }
    token = sessions.create_session(runtime.context.userId, recipe)
    return f"{PUBLIC_URL}/cook/{token}"
