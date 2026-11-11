import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
ALLOWED_USER_IDS = [ int(i) for i in os.environ["ALLOWED_USER_IDS"].split(",") ]