from langchain.tools import tool, ToolRuntime

from src.agent.context import Context
from src.db import inventory

@tool
def shopping_list (runtime: ToolRuntime[Context]) -> list[dict] | str:
    """Generate the user's shopping list: the products at or below the minimum quantity they want to have.
    Each one has the quantity they have now and the minimum."""
    rows = inventory.low_stock(runtime.context.userId)
    if not rows:
        return "Nothing is below its minimum. The user may not have set minimums yet."
    return [
        { "name": r["productName"], "have": r["productQuantity"], "minimum": r["productMinQuantity"], "unit": r["productUnit"] }
        for r in rows
    ]
