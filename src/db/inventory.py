from src.db import execute, query

def add_item (userId, name, quantity, unit, expires_at=None):
    execute("inventory:add", (userId, name, quantity, unit, expires_at))

def list_items (userId):
    return query("inventory:list", (userId,))

# without quantity the whole product is removed
def remove_item (userId, name, unit, quantity=None):
    if quantity is None:
        execute("inventory:delete", (userId, name, unit))
    else:
        execute("inventory:remove", (quantity, userId, name, unit))
        execute("inventory:prune", (userId,))

def expiring_soon (userId, days=3):
    return query("inventory:expiring", (userId, f"+{days} days"))
