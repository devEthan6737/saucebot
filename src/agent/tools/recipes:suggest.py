from langchain.tools import tool, ToolRuntime

from src.agent.context import Context
from src.agent.recipes import generate_recipe

@tool
def suggest_recipe (runtime: ToolRuntime[Context], preferences: str | None = None) -> dict | str:
    """Design a recipe based on the products in the user's inventory, prioritizing the ones that expire soon.
    Optional preferences, for example 'vegetarian' or 'something quick'.
    It returns the ingredients only, it never explains how to cook it."""

    recipe = generate_recipe(runtime.context.userId, preferences)

    if recipe is None:
        return "The inventory is empty, there is nothing to cook with."
    return recipe.model_dump()
