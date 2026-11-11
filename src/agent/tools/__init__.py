from importlib import import_module

# file names use a colon (inventory:add.py) so they can't be imported with a normal import
def load (name: str):
    return import_module(f"src.agent.tools.{name}")

tools = [
    load("inventory:add").add_item,
    load("inventory:list").list_items,
    load("inventory:remove").remove_item,
    load("inventory:expiring").expiring_soon,
]
