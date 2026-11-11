import re

# every way of writing a unit maps to one canonical unit, so "litros" and "l" are the same product
units = {
    "l": "l", "lt": "l", "litro": "l", "litros": "l",
    "ml": "ml", "mililitro": "ml", "mililitros": "ml",
    "g": "g", "gr": "g", "gramo": "g", "gramos": "g",
    "kg": "kg", "kilo": "kg", "kilos": "kg", "kilogramo": "kg", "kilogramos": "kg",
    "unidad": "unidad", "unidades": "unidad", "ud": "unidad", "uds": "unidad", "u": "unidad", "pieza": "unidad", "piezas": "unidad",
}

# lowercase, no extra spaces
def normalize_name (name: str) -> str:
    return re.sub(r"\s+", " ", name).strip().lower()

# canonical unit if we know it, otherwise just cleaned up
def normalize_unit (unit: str) -> str:
    unit = normalize_name(unit).rstrip(".")
    return units.get(unit, unit)
