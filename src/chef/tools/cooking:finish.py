from langchain.tools import tool, ToolRuntime

from src.chef.context import ChefContext
from src.db import inventory, sessions

@tool
def finish_cooking (runtime: ToolRuntime[ChefContext]) -> str:
    """Call it when the user confirms the dish is finished. It subtracts the ingredients of the recipe
    from the user's inventory and closes the cooking session."""
    context = runtime.context

    for ingredient in context.recipe.get("in_stock", []):
        inventory.remove_item(context.userId, ingredient["name"], ingredient["unit"], ingredient["quantity"])

    sessions.delete_session(context.token)
    return "Cooking finished, the inventory is updated and the session is closed."
