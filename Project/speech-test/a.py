import speech_recognition as sr

def take_voice_input():
    # Initialize recognizer class
    recognizer = sr.Recognizer()

    # Capture microphone input
    with sr.Microphone() as source:
        print("Please speak...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio_data = recognizer.listen(source)

        try:
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio_data)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
            return None
        except sr.RequestError as e:
            print("Error with the service; {0}".format(e))
            return None

if __name__ == "__main__":
    take_voice_input()
