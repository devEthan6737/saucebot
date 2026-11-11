from importlib import import_module

# file names use a colon (cooking:finish.py) so they can't be imported with a normal import
def load (name: str):
    return import_module(f"src.chef.tools.{name}")

tools = [
    load("cooking:finish").finish_cooking,
]
