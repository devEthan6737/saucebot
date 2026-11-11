from langchain.tools import tool, ToolRuntime

from src.agent.context import Context
from src.db import inventory

@tool
def add_item (name: str, quantity: float, unit: str, runtime: ToolRuntime[Context], expires_at: str | None = None, min_quantity: float | None = None) -> str:
    """Add a product to the user's inventory. If it already exists with the same unit, the quantity is added to it.
    expires_at is optional and must be in YYYY-MM-DD format.
    min_quantity is optional: the amount the user always wants to have at home, below it the product goes to the shopping list.
    To only set a minimum, use quantity 0."""
    inventory.add_item(runtime.context.userId, name, quantity, unit, expires_at, min_quantity)
    return f"Added {quantity} {unit} of {name}"
