from datetime import date

from pydantic import BaseModel, Field

from src.agent.model import model
from src.db import inventory

class Ingredient (BaseModel):
    name: str
    quantity: float
    unit: str

class Recipe (BaseModel):
    name: str
    description: str = Field(description="One short sentence about the dish")
    servings: int
    in_stock: list[Ingredient] = Field(description="Ingredients the user already has, never more than the available quantity")
    missing: list[Ingredient] = Field(description="Ingredients the user would need to buy")

prompt = """Design one recipe using the products the user has at home.
Prefer the products that expire first. Use only the products listed below for the in_stock ingredients, \
with the same names and units and never more than the available quantity. \
Anything else the recipe needs goes in missing, keep it to a minimum.
Do NOT write the cooking steps, only the recipe name, description, servings and ingredients.

Today is {today}.
Inventory (name, quantity, unit, expires):
{items}

User preferences: {preferences}"""

# returns None if the user has nothing in the inventory
def generate_recipe (userId: int, preferences: str | None = None) -> Recipe | None:
    rows = inventory.list_items(userId)
    if not rows:
        return None

    # the ones that expire first go first, the ones without date go last
    rows = sorted(rows, key=lambda r: (r["productExpiresAt"] is None, r["productExpiresAt"] or ""))
    items = "\n".join(
        f"- {r['productName']}, {r['productQuantity']}, {r['productUnit']}, {r['productExpiresAt'] or 'no date'}"
        for r in rows
    )

    return model.with_structured_output(Recipe).invoke(prompt.format(
        today=date.today().isoformat(),
        items=items,
        preferences=preferences or "none",
    ))
