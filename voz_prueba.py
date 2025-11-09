import speech_recognition as sr
import pyttsx3

# Inicializa el motor de voz
engine = pyttsx3.init()
engine.say("Hola José, estoy lista para escuchar tu voz.")
engine.runAndWait()

# Inicializa el reconocimiento de voz
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Di algo...")
    audio = r.listen(source)

try:
    texto = r.recognize_google(audio, language="es-ES")
    print("Has dicho:", texto)
    engine.say("Has dicho " + texto)
    engine.runAndWait()
except:
    engine.say("No entendí lo que dijiste.")
    engine.runAndWait()
