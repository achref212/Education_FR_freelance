from gtts import gTTS
import base64
from io import BytesIO
import speech_recognition as sr

def text_to_audio_base64(text):
    tts = gTTS(text, lang="fr")
    buffer = BytesIO()
    tts.write_to_fp(buffer)
    audio_bytes = buffer.getvalue()
    return base64.b64encode(audio_bytes).decode("utf-8")

def speech_to_text(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    return r.recognize_whisper(audio, language="fr")  # FREE LOCAL MODEL
