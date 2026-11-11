import io
import threading
import wave

from piper import PiperVoice

from src.config import PIPER_VOICE_PATH

# the voice is loaded the first time it is needed
_voice = None

# piper is not thread safe, so one sentence at a time
_lock = threading.Lock()

def voice_exists () -> bool:
    return PIPER_VOICE_PATH.exists()

def get_voice ():
    global _voice
    if _voice is None:
        _voice = PiperVoice.load(str(PIPER_VOICE_PATH))
    return _voice

# text to a wav file in memory
def synthesize (text: str) -> bytes:
    with _lock:
        voice = get_voice()
        pcm = b"".join(chunk.audio_int16_bytes for chunk in voice.synthesize(text))
        rate = voice.config.sample_rate

    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(rate)
        f.writeframes(pcm)
    return buffer.getvalue()
