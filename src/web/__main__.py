import uvicorn

from src.config import WEB_HOST, WEB_PORT

uvicorn.run("src.web:app", host=WEB_HOST, port=WEB_PORT)
