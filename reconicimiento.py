import speech_recognition as sr

def reconocer_voz():
    # Crear un reconocedor de voz
    recognizer = sr.Recognizer()

    # Usar el micrófono como fuente de audio
    with sr.Microphone() as source:
        print("Por favor, hable ahora...")
        # Ajustar el ruido ambiental
        recognizer.adjust_for_ambient_noise(source)
        # Escuchar el audio del micrófono
        audio = recognizer.listen(source)

    try:
        # Usar el reconocimiento de Google para convertir el audio en texto
        texto = recognizer.recognize_google(audio, language="es-ES")
        print("Usted dijo: " + texto)


    except sr.UnknownValueError:
        print("No se pudo entender el audio.")
    except sr.RequestError as err:
        print(f"Error al solicitar resultados del servicio de reconocimiento; {err}")
if __name__ == "__main__":

    reconocer_voz()

import sounddevice as sd

from scipy.io.wavfile import write

def grabar_voz(nombre_archivo="mi_voz.wav", duracion=5):
    frecuencia_muestreo = 44100  # Frecuencia de muestreo en Hz
    print("Grabando...")
    grabacion = sd.rec(int(duracion * frecuencia_muestreo), samplerate=frecuencia_muestreo, channels=2)
    sd.wait()  # Esperar a que la grabación termine
    write(nombre_archivo, frecuencia_muestreo, grabacion)  # Guardar la grabación en un archivo WAV
    print("Grabación terminada y guardada en " + nombre_archivo)

if __name__ == "__main__":
    grabar_voz() 

import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer
from resemblyzer import VoiceEncoder, preprocess_wav
import json
import torch

# Cargar modelo de voz (Vosk)
model = Model("model")
rec = KaldiRecognizer(model, 16000)

# Crear codificador de voz (Resemblyzer)
encoder = VoiceEncoder()

# Procesar tu voz de referencia
your_voice = preprocess_wav("mi_voz.wav")
your_embedding = encoder.embed_utterance(your_voice)

def escuchar():
    samplerate = 16000
    with sd.InputStream(samplerate=samplerate, channels=1, dtype='int16') as stream:
        print("Escuchando... (solo escribirá cuando tú hables)")
        while True:
            data, _ = stream.read(4000)
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if not text:
                    continue

                # Analizar similitud de voz
                audio_np = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
                embedding = encoder.embed_utterance(audio_np)
                similarity = np.dot(your_embedding, embedding)

                # Ajusta el umbral según tu micrófono
                if similarity > 0.75:
                    print("🗣️ Tú:", text)
                else:
                    print("(Ignorado, no eres tú)")

if __name__ == "__main__":
    escuchar()