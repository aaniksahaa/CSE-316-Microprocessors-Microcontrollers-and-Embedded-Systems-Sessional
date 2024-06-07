import speech_recognition as sr
import pyttsx3

# Initialize recognizer class
recognizer = sr.Recognizer()

def take_voice_input():
    # Capture microphone input
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.2)  # Adjust for ambient noise
        audio_data = recognizer.listen(source)

        text = None

        try:
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio_data)
            #print("You said:", text)
            #return text
        except sr.UnknownValueError:
            #print("Sorry, could not understand audio.")
            text = None
            #return None
        except sr.RequestError as e:
            text = None
            #print("Error with the service; {0}".format(e))
            #return None

        return text 

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    print("Please speak...")
    while True:
        user_input = take_voice_input()
        if user_input:
            response = "You said: " + user_input
            print(response)
            #speak(response)
