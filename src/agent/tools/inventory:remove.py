from langchain.tools import tool, ToolRuntime

from src.agent.context import Context
from src.db import inventory

@tool
def remove_item (name: str, unit: str, runtime: ToolRuntime[Context], quantity: float | None = None) -> str:
    """Remove a product from the user's inventory. Without quantity the whole product is removed,
    with quantity only that amount is subtracted."""
    inventory.remove_item(runtime.context.userId, name, unit, quantity)
    return f"Removed {name}" if quantity is None else f"Removed {quantity} {unit} of {name}"
