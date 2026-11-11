import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
DEEPSEEK_API_KEY = os.environ["DEEPSEEK_API_KEY"]
ALLOWED_USER_IDS = [ int(i) for i in os.environ["ALLOWED_USER_IDS"].split(",") ]