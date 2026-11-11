from dataclasses import dataclass

# data passed to the chef on every call, its tools read it from runtime.context
@dataclass
class ChefContext:
    token: str
    userId: int
    recipe: dict
