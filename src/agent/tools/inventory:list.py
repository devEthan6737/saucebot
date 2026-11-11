from langchain.tools import tool, ToolRuntime

from src.agent.context import Context
from src.db import inventory

@tool
def list_items (runtime: ToolRuntime[Context]) -> list[dict]:
    """List everything in the user's inventory."""
    return [ dict(row) for row in inventory.list_items(runtime.context.userId) ]
