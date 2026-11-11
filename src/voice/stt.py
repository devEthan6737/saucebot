import json
import subprocess
import wave
from pathlib import Path

from vosk import Model, KaldiRecognizer, SetLogLevel

from src.config import VOSK_MODEL_PATH

SetLogLevel(-1)

SAMPLE_RATE = 16000

# the model is heavy, so it is loaded the first time it is needed
_model = None

def model_exists () -> bool:
    return VOSK_MODEL_PATH.exists()

def get_model ():
    global _model
    if _model is None:
        _model = Model(str(VOSK_MODEL_PATH))
    return _model

# a new recognizer for a stream of 16kHz mono pcm audio
def new_recognizer ():
    return KaldiRecognizer(get_model(), SAMPLE_RATE)

# telegram sends ogg/opus, vosk needs wav 16kHz mono
def transcribe (audio: Path) -> str:
    wav = audio.with_suffix(".wav")
    subprocess.run(["ffmpeg", "-y", "-i", str(audio), "-ar", str(SAMPLE_RATE), "-ac", "1", str(wav)], check=True, capture_output=True)

    recognizer = new_recognizer()
    with wave.open(str(wav), "rb") as f:
        while data := f.readframes(4000):
            recognizer.AcceptWaveform(data)

    return json.loads(recognizer.FinalResult())["text"]
