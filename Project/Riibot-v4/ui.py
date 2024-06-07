import tkinter as tk
from tkinter import ttk
import threading
import time
from settings import *

# Initialize is_on variable
CONTROL_STATE = "OFF"

# Function to update console with MAX_ABS_SPEED
def update_console():
    while True:
        print(f"MAX_ABS_SPEED: {MAX_ABS_SPEED}", end=" ")
        print(f"ROTATION_CONST_SPEED: {ROTATION_CONST_SPEED}", end=" ")
        print(f"CONTROL_STATE: {CONTROL_STATE}")
        time.sleep(1)

# UI thread function
def run_ui():
    # Function to handle button clicks
    def start():
        global CONTROL_STATE
        CONTROL_STATE = "ON"
        state_text.set("State: ON")

    def stop():
        global CONTROL_STATE
        CONTROL_STATE = "OFF"
        state_text.set("State: OFF")

    def reset():
        global CONTROL_STATE
        CONTROL_STATE = "RESET"
        state_text.set("State: RESET")

    # Function to update max speed label
    def update_max_speed_label(value):
        global MAX_ABS_SPEED
        max_speed_value.set(int(float(value)))
        MAX_ABS_SPEED = int(float(value))

    # Function to update rotation speed label
    def update_rotation_speed_label(value):
        global ROTATION_CONST_SPEED
        rotation_speed_value.set(int(float(value)))
        ROTATION_CONST_SPEED = int(float(value))

    # Create Tkinter window
    window = tk.Tk()
    window.title("Control Panel")

    # Set window dimensions
    window_width = 600
    window_height = 400

    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate x and y coordinates for the window to be centered
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set window size and position
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Define colors
    button_bg_color = 'white'
    hover_color = '#87CEFA'  # Bluish color

    # Create style for start button
    start_style = ttk.Style()
    start_style.configure('Start.TButton', background='green', foreground='black', font=('Helvetica', 16),
                          bordercolor='black', borderwidth=3,
                          focuscolor=hover_color, lightcolor=hover_color, darkcolor=hover_color)

    # Create style for stop button
    stop_style = ttk.Style()
    stop_style.configure('Stop.TButton', background='red', foreground='black', font=('Helvetica', 16),
                          bordercolor='black', borderwidth=3,
                          focuscolor=hover_color, lightcolor=hover_color, darkcolor=hover_color)

    # Create Start button
    start_button = ttk.Button(window, text="Start", style='Start.TButton', command=start)
    start_button.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    # Create Stop button
    stop_button = ttk.Button(window, text="Stop", style='Stop.TButton', command=stop)
    stop_button.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    # Create Reset button
    reset_button = ttk.Button(window, text="Reset", style='Stop.TButton', command=reset)
    reset_button.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    # Create text box to display state
    state_text = tk.StringVar()
    state_label = ttk.Label(window, textvariable=state_text, font=('Helvetica', 12))
    state_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
    state_text.set("State: OFF")  # Initial state

    # Create sliders
    max_speed_label = ttk.Label(window, text="Max Speed:", font=('Helvetica', 10))
    max_speed_label.place(relx=0.3, rely=0.4, anchor=tk.E)

    max_speed_value = tk.StringVar()
    max_speed_value_label = ttk.Label(window, textvariable=max_speed_value, font=('Helvetica', 14))
    max_speed_value_label.place(relx=0.7, rely=0.4, anchor=tk.W)

    max_speed_slider = ttk.Scale(window, from_=0, to=250, orient=tk.HORIZONTAL, length=200, command=update_max_speed_label)
    max_speed_slider.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    max_speed_slider.set(MAX_ABS_SPEED)

    rotation_speed_label = ttk.Label(window, text="Rotation Constant Speed:", font=('Helvetica', 10))
    rotation_speed_label.place(relx=0.3, rely=0.5, anchor=tk.E)

    rotation_speed_value = tk.StringVar()
    rotation_speed_value_label = ttk.Label(window, textvariable=rotation_speed_value, font=('Helvetica', 14))
    rotation_speed_value_label.place(relx=0.7, rely=0.5, anchor=tk.W)

    rotation_speed_slider = ttk.Scale(window, from_=0, to=120, orient=tk.HORIZONTAL, length=200, command=update_rotation_speed_label)
    rotation_speed_slider.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    rotation_speed_slider.set(ROTATION_CONST_SPEED)

    # Start the Tkinter event loop
    window.mainloop()

# Start the UI thread
ui_thread = threading.Thread(target=run_ui)
ui_thread.daemon = True
ui_thread.start()

# Main thread runs the console update function
update_console()
