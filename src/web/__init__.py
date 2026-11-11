import asyncio
import json
import logging
import re
import threading
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse, Response

from src import chef
from src.config import WEB_HOST, WEB_PORT
from src.db import sessions
from src.voice import stt, tts

log = logging.getLogger("saucebot.web")

static = Path(__file__).parent / "static"

# the models take a few seconds to load, better at startup than in the middle of a session
@asynccontextmanager
async def lifespan (app: FastAPI):
    sessions.purge_sessions()
    await asyncio.to_thread(stt.get_model)
    await asyncio.to_thread(tts.get_voice)
    yield

app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)

# splits the text received so far into finished sentences and the rest
def split_sentences (buffer: str):
    parts = re.split(r"(?<=[.!?…:])\s+|\n+", buffer)
    return parts[:-1], parts[-1]

# the voice must not read markdown symbols
def clean (sentence: str) -> str:
    return re.sub(r"[*_#`>~]", "", sentence).strip()

@app.get("/cook/{token}")
async def page (token: str):
    if sessions.get_session(token) is None:
        return Response("Esta sesión de cocina no existe o ha caducado.", status_code=404)
    return FileResponse(static / "index.html", headers={ "Cache-Control": "no-store" })

@app.get("/api/cook/{token}")
async def recipe (token: str):
    session = sessions.get_session(token)
    if session is None:
        return JSONResponse({ "error": "not found" }, status_code=404)
    return session["recipe"]

@app.websocket("/ws/{token}")
async def live (ws: WebSocket, token: str):
    session = sessions.get_session(token)
    if session is None:
        await ws.close(code=4404)
        return

    await ws.accept()

    recognizer = stt.new_recognizer()
    listening = False
    partial = ""

    # the chef turn that is running, it is a task so the chef can be interrupted while it talks
    current = None

    def busy ():
        return current is not None and not current.done()

    # one sentence of the chef: the text and the audio
    async def say (sentence: str):
        sentence = clean(sentence)
        if sentence:
            await ws.send_json({ "type": "chef", "text": sentence })
            await ws.send_bytes(await asyncio.to_thread(tts.synthesize, sentence))

    # tells the client that the turn is over, or that the whole cooking is over
    async def end_turn ():
        over = sessions.get_session(token) is None
        await ws.send_json({ "type": "done" if over else "turn_end" })
        if over:
            chef.forget(token)
            await ws.close()

    # the chef answers sentence by sentence, so it starts talking before it has finished writing
    async def turn (text: str):
        buffer = ""
        try:
            async for delta in chef.talk(token, session["userId"], session["recipe"], text):
                buffer += delta
                ready, buffer = split_sentences(buffer)
                for sentence in ready:
                    await say(sentence)
            await say(buffer)
        except asyncio.CancelledError:
            raise
        except Exception:
            log.exception("chef turn failed")
            await ws.send_json({ "type": "error", "text": "He tenido un problema, repítelo por favor." })

        await end_turn()

    def start_turn (text: str):
        nonlocal current, listening
        listening = False
        current = asyncio.create_task(turn(text))

    try:
        while True:
            message = await ws.receive()
            if message["type"] == "websocket.disconnect":
                break

            audio = message.get("bytes")
            if audio is not None:
                if not listening or busy():
                    continue

                if recognizer.AcceptWaveform(audio):
                    text = json.loads(recognizer.Result())["text"]
                    if text:
                        listening = False
                        await ws.send_json({ "type": "user", "text": text })
                        start_turn(text)
                else:
                    now = json.loads(recognizer.PartialResult())["partial"]
                    if now != partial:
                        partial = now
                        await ws.send_json({ "type": "partial", "text": partial })
                continue

            data = json.loads(message["text"])

            if data["type"] == "interrupt":
                if busy():
                    current.cancel()
                    await asyncio.gather(current, return_exceptions=True)
                    await end_turn()
            elif busy():
                continue
            elif data["type"] == "start":
                start_turn("Hola, empecemos.")
            elif data["type"] == "listening":
                recognizer = stt.new_recognizer()
                partial = ""
                listening = True
            elif data["type"] == "text" and data.get("text", "").strip():
                start_turn(data["text"].strip())
    except (WebSocketDisconnect, RuntimeError):
        pass
    finally:
        if busy():
            current.cancel()
        if sessions.get_session(token) is None:
            chef.forget(token)

# starts the web in a thread, so it can run next to the telegram bot in the same process
# returns the server, set should_exit to stop it
def start ():
    server = uvicorn.Server(uvicorn.Config(app, host=WEB_HOST, port=WEB_PORT, log_level="warning"))
    threading.Thread(target=server.run, daemon=True).start()
    return server
