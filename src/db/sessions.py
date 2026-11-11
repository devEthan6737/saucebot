import json
import secrets

from src.db import execute, query

# a cooking session is the recipe plus a random token that works as the link to the live chef
def create_session (userId: int, recipe: dict, hours: int = 3) -> str:
    token = secrets.token_urlsafe(24)
    execute("sessions:add", (token, userId, json.dumps(recipe), f"+{hours} hours"))
    return token

# None if it doesn't exist or has expired
def get_session (token: str) -> dict | None:
    rows = query("sessions:get", (token,))
    if not rows:
        return None
    return { "token": token, "userId": rows[0]["userId"], "recipe": json.loads(rows[0]["recipe"]) }

def delete_session (token: str):
    execute("sessions:delete", (token,))

# removes the expired ones
def purge_sessions ():
    execute("sessions:purge")
