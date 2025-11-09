# voice_assistant.py
# 🟣 Asistente de voz A.L.I.C.E. con escucha y respuesta por voz + ChatGPT integrado

import os
import speech_recognition as sr
from elevenlabs import ElevenLabs
from openai import OpenAI
from dotenv import load_dotenv

# Cargar las claves desde el archivo .env
load_dotenv()

# 🔹 Configuración de APIs
ELEVEN_API_KEY = os.getenv("sk_1b381e672368f29bfd55d7cdb05cadb99b2cb2d8242815d1")
OPENAI_API_KEY = os.getenv("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")

client = ElevenLabs(api_key=ELEVEN_API_KEY)
chat_client = OpenAI(api_key=OPENAI_API_KEY)

# 🔹 Configuración de voz
VOICE_ID = "EYBbN7OENxAX5QX56IiW"

# 🔹 Identidad del asistente
ASISTENTE_NOMBRE = "Alice"
ASISTENTE_GENERO = "femenino"
ASISTENTE_PERSONALIDAD = (
    "Eres Alice, una asistente de voz femenina, cálida, profesional e inteligente. "
    "Hablas en tono amable y natural, con voz empática."
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

# 🔹 Escuchar desde micrófono
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

# 🔹 Obtener respuesta de ChatGPT
def responder_chatgpt(pregunta):
    if not pregunta:
        return "No entendí lo que dijiste."

    response = chat_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": ASISTENTE_PERSONALIDAD},
            {"role": "user", "content": pregunta}
        ]
    )

    respuesta = response.choices[0].message.content
    return respuesta

# 🔹 Programa principal
if __name__ == "__main__":
    print(f"🔊 Iniciando {ASISTENTE_NOMBRE} ({ASISTENTE_GENERO})...\n")
    hablar("Hola Oscar, soy Alice. Estoy lista para conversar contigo.")

    while True:
        texto_usuario = escuchar()
        if not texto_usuario:
            continue

        if any(saludo in texto_usuario for saludo in ["salir", "adiós", "chao", "terminar"]):
            hablar("Hasta luego Oscar. Que tengas un excelente día.")
            break
        else:
            respuesta = responder_chatgpt(texto_usuario)
            hablar(respuesta)

