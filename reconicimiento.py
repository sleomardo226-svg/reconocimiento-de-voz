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
        print("No se pudo entender el audio; {0}".format(e))

if __name__ == "__main__":

    reconocer_voz()


