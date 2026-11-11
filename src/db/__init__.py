import sqlite3
from pathlib import Path

root_path = Path(__file__).parents[2]

# allow using the connection from other threads cz telegram bots are async
db = sqlite3.connect(root_path / "saucebot.db", check_same_thread=False)
db.row_factory = sqlite3.Row

def _sql (name: str):
    return (root_path / "src/db/sql" / f"{name}.sql").read_text()

# run a script without params (create tables, etc)
def run (name: str):
    db.executescript(_sql(name))

# run a single statement with params and commit (insert, update, delete)
def execute (name: str, params=()):
    with db:
        db.execute(_sql(name), params)

# run a single select with params and return all rows
def query (name: str, params=()):
    return db.execute(_sql(name), params).fetchall()


# start scripts
run("inventory:create")
