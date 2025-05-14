# STT.py
import speech_recognition as sr
import pyaudio
from gtts import gTTS



print("Démarrage de la reconnaissance vocale...")
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Parlez maintenant...")
    audio_data = r.listen(source)
    print("Traitement de l'audio...")

try:
    result = r.recognize_google(audio_data, language="fr-FR")
    print(result)  # On imprime dans stdout au lieu d’écrire dans un fichier
except Exception as e:
    print(f"[ERREUR] {e}")
    exit(1)  # code d'erreur en cas d'échec
