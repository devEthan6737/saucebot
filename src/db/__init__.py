import sqlite3
from pathlib import Path

root_path = Path(__file__).parents[2]

# allow using the connection from other threads cz telegram bots are async
db = sqlite3.connect(root_path / "saucebot.db", check_same_thread=False)
db.row_factory = sqlite3.Row

# function to run db scripts located in ./sql
def run (name: str):
    db.executescript((root_path / "src/db/sql" / f"{name}.sql").read_text())


# start scripts
run("inventory:create")