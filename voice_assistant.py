# voice_assistant.py
# 🟣 Asistente de voz A.L.I.C.E. con escucha y respuesta por voz

import os
import speech_recognition as sr
from elevenlabs import ElevenLabs

# 🔹 Configuración del API de ElevenLabs
ELEVEN_API_KEY = "sk_1b381e672368f29bfd55d7cdb05cadb99b2cb2d8242815d1"
client = ElevenLabs(api_key=ELEVEN_API_KEY)

# 🔹 Voz femenina fija
VOICE_ID = "EYBbN7OENxAX5QX56IiW"

# 🔹 Identidad del asistente
ASISTENTE_NOMBRE = "Alice"
ASISTENTE_GENERO = "femenino"
ASISTENTE_PERSONALIDAD = (
    "Soy Alice, tu asistente de voz. Tengo una voz cálida y profesional. "
    "Estoy aquí para ayudarte en lo que necesites."
)

# 🔹 Función para hablar
def hablar(texto):
    print(f"[{ASISTENTE_NOMBRE} ({ASISTENTE_GENERO})]: {texto}")

    audio = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        model_id="eleven_multilingual_v2",
        text=texto,
        voice_settings={
            "stability": 0.45,
            "similarity_boost": 0.85,
            "style": 0.5,
            "use_speaker_boost": True
        }
    )

    audio_path = "voz_actual.mp3"
    with open(audio_path, "wb") as f:
        for chunk in audio:
            if chunk:
                f.write(chunk)

    os.system("start " + audio_path)

# 🔹 Función para escuchar desde el micrófono
def escuchar():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Escuchando... (habla ahora)")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        texto = recognizer.recognize_google(audio, language="es-ES")
        print(f"Tú: {texto}")
        return texto.lower()
    except sr.UnknownValueError:
        print("❌ No entendí lo que dijiste.")
        return None
    except sr.RequestError:
        print("⚠️ Error con el servicio de reconocimiento.")
        return None

# 🔹 Programa principal
if __name__ == "__main__":
    print(f"🔊 Iniciando {ASISTENTE_NOMBRE} ({ASISTENTE_GENERO})...\n")
    hablar("Hola Oscar, soy Alice. Estoy lista para conversar contigo.")

    while True:
        texto_usuario = escuchar()
        if texto_usuario:
            if "salir" in texto_usuario or "adiós" in texto_usuario or "chao" in texto_usuario:
                hablar("Hasta luego Oscar. Que tengas un excelente día.")
                break
            elif "cómo estás" in texto_usuario:
                hablar("Estoy muy bien, gracias por preguntar. ¿Y tú?")
            elif "tu nombre" in texto_usuario:
                hablar("Me llamo Alice, tu asistente de voz personal.")
            elif "ayuda" in texto_usuario:
                hablar("Puedo escucharte y responderte por voz. Solo dime qué necesitas.")
            else:
                hablar(f"Entendí que dijiste: {texto_usuario}. Aún estoy aprendiendo a responder más preguntas.")
