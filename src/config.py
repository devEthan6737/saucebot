import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
DEEPSEEK_API_KEY = os.environ["DEEPSEEK_API_KEY"]
ALLOWED_USER_IDS = [ int(i) for i in os.environ["ALLOWED_USER_IDS"].split(",") ]

# folder of the vosk model used to transcribe voice notes
VOSK_MODEL_PATH = Path(os.environ.get("VOSK_MODEL_PATH", Path(__file__).parents[1] / "models" / "vosk-model-small-es-0.42"))

# piper voice used by the live chef
PIPER_VOICE_PATH = Path(os.environ.get("PIPER_VOICE_PATH", Path(__file__).parents[1] / "models" / "piper" / "es_ES-davefx-medium.onnx"))

# live chef web: where it listens and the address the links sent to Telegram point to
WEB_HOST = os.environ.get("WEB_HOST", "127.0.0.1")
WEB_PORT = int(os.environ.get("WEB_PORT", "8000"))
PUBLIC_URL = os.environ.get("PUBLIC_URL", f"http://localhost:{WEB_PORT}").rstrip("/")
