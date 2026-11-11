from langchain.tools import tool, ToolRuntime

from src.agent.context import Context
from src.db import inventory

@tool
def add_item (name: str, quantity: float, unit: str, runtime: ToolRuntime[Context], expires_at: str | None = None) -> str:
    """Add a product to the user's inventory. If it already exists with the same unit, the quantity is added to it.
    expires_at is optional and must be in YYYY-MM-DD format."""
    inventory.add_item(runtime.context.userId, name, quantity, unit, expires_at)
    return f"Added {quantity} {unit} of {name}"
