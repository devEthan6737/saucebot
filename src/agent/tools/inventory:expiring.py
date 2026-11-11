from langchain.tools import tool, ToolRuntime

from src.agent.context import Context
from src.db import inventory

@tool
def expiring_soon (runtime: ToolRuntime[Context], days: int = 3) -> list[dict]:
    """List the products that expire in the next N days (3 by default), including the ones already expired."""
    return [ dict(row) for row in inventory.expiring_soon(runtime.context.userId, days) ]
