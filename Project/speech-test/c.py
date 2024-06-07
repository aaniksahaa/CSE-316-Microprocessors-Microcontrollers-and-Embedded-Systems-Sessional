import tkinter as tk
import speech_recognition as sr

def record_voice():
    # Function to record voice input
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        #print("Recording...")
        display_text.config(text="Recording...")
        audio_data = recognizer.listen(source, timeout=10)
        
    try:
        text = recognizer.recognize_google(audio_data)
        display_text.config(text="Text: " + text)
    except sr.UnknownValueError:
        display_text.config(text="Sorry, could not understand audio.")
    except sr.RequestError as e:
        display_text.config(text="Error with the service; {0}".format(e))

# Create the main window
root = tk.Tk()
root.title("Voice Input")
root.geometry("300x200")

# Create the microphone icon
canvas = tk.Canvas(root, width=100, height=100)
canvas.pack()

# Draw microphone icon (two circles)
canvas.create_oval(25, 25, 75, 75, outline="black", fill="black") # Microphone
canvas.create_oval(40, 40, 60, 60, outline="black", fill="white") # Sound

# Create a button with the microphone icon
mic_button = tk.Button(root, text="Record", command=record_voice)
mic_button.pack(pady=10)

# Display recognized text
display_text = tk.Label(root, text="Text: ")
display_text.pack()

root.mainloop()
