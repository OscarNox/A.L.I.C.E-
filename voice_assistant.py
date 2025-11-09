# voice_assistant.py
# 🟣 Asistente de voz A.L.I.C.E. – versión estable con voz femenina fija

from elevenlabs import ElevenLabs
import os

# 🔹 Paso 1: Configurar tu API Key (con permiso de texto a voz)
ELEVEN_API_KEY = "sk_1b381e672368f29bfd55d7cdb05cadb99b2cb2d8242815d1"  # <-- tu API Key
client = ElevenLabs(api_key=ELEVEN_API_KEY)

# 🔹 Paso 2: Configurar la voz femenina fija
VOICE_ID = "EYBbN7OENxAX5QX56IiW"  # <-- tu voz femenina elegida en ElevenLabs

# 🔹 Paso 3: Definir identidad del asistente
ASISTENTE_NOMBRE = "Alice"
ASISTENTE_GENERO = "femenino"
ASISTENTE_PERSONALIDAD = (
    "Soy Alice, tu asistente de voz. "
    "Tengo una voz cálida y profesional. "
    "Estoy aquí para ayudarte en lo que necesites."
)

def hablar(texto):
    """
    Convierte texto en voz femenina fija usando ElevenLabs y lo reproduce automáticamente.
    """
    print(f"[{ASISTENTE_NOMBRE} ({ASISTENTE_GENERO})]: {texto}")

    audio = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        model_id="eleven_multilingual_v2",  # modelo de voz más fluido
        text=texto,
        voice_settings={
            "stability": 0.45,          # controla consistencia emocional
            "similarity_boost": 0.85,   # mantiene el timbre natural
            "style": 0.5,               # suavidad
            "use_speaker_boost": True   # potencia la claridad
        }
    )

    # Guardar el audio en un archivo temporal
    audio_path = "voz_actual.mp3"
    with open(audio_path, "wb") as f:
        for chunk in audio:
            if chunk:
                f.write(chunk)

    # Reproducir el audio automáticamente
    os.system("start " + audio_path)  # En Windows usa 'start'; en Mac usa 'open', en Linux 'xdg-open'


# 🔹 Ejemplo de uso
if __name__ == "__main__":
    print(f"🔊 Iniciando {ASISTENTE_NOMBRE} ({ASISTENTE_GENERO})...\n")
    hablar("Hola Oscar, soy Alice, tu asistente de voz. Estoy lista para ayudarte con lo que necesites. Puedes pedirme que hable, piense o te ayude con tareas paso a paso.")
 
