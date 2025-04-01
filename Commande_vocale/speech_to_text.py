
import os
import speech_recognition as sr
import pyaudio
from gtts import gTTS

def text_to_speech(text):
    
    # Initialize gTTS with the text to convert
    speech = gTTS(text, lang="fr", slow=False)
    # Save the audio file to a temporary file
    speech_file = 'speech.mp3'
    speech.save(speech_file)
    # Play the audio file
    os.system('afplay ' + speech_file)
## CELLULE ASSISTANT VOCAL
r = sr.Recognizer()
micro = sr.Microphone()
with micro as source:
    print("Speak!")
    audio_data = r.listen(source)
    print("End!")
transcription = r.recognize_google(audio_data, language="fr-FR")
# pour une reconnaissance de la parole en anglais
#result = r.recognize_google(audio_data, language="en-EN")
print ("Vous avez dit : ", transcription)
#...
#message_reponse = "je vous ai compris !!"
#text_to_speech(message_reponse)

#tokens=normaliser_transcription(transcription)

# Sauvegarder la transcription dans un fichier
with open("Commande_vocale/transcription.txt", "w") as file:
    file.write(transcription)

