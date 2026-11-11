from src.db import execute, query
from src.db.normalize import normalize_name, normalize_unit

# min_quantity is the amount the user wants to always have, below it the product goes to the shopping list
def add_item (userId, name, quantity, unit, expires_at=None, min_quantity=None):
    execute("inventory:add", (userId, normalize_name(name), quantity, normalize_unit(unit), expires_at, min_quantity))

def list_items (userId):
    return query("inventory:list", (userId,))

# without quantity the whole product is removed
def remove_item (userId, name, unit, quantity=None):
    name, unit = normalize_name(name), normalize_unit(unit)

    if quantity is None:
        execute("inventory:delete", (userId, name, unit))
    else:
        execute("inventory:remove", (quantity, userId, name, unit))
        execute("inventory:prune", (userId,))

def expiring_soon (userId, days=3):
    return query("inventory:expiring", (userId, f"+{days} days"))

# the shopping list: products at or below the minimum the user wants to have
def low_stock (userId):
    return query("inventory:low", (userId,))
