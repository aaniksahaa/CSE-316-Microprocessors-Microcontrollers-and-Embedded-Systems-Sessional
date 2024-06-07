import math
import cv2
import numpy as np
import heapq
import random
import websocket
import threading
from model import Linear_QNet, QTrainer
import torch

import tkinter as tk
from tkinter import ttk

from util import *
from settings import *


# Initialize is_on variable
CONTROL_STATE = "ON"

# Reinforcement Learning Model

model = Linear_QNet(19, 256, 2)
model.load_state_dict(torch.load('model/model-100.pth'))
model.eval()

# Websocket Connection

is_connected = False  

# Define the WebSocket server address
server_address = "ws://" + IP + ":" + PORT + "/"

# Enable the Websocket Connection and retrieve the connection instance at ws
ws = websocket.WebSocketApp(server_address,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)


#global virtual object list 
# these will be considered as destinations one by one 
objects = []

def drawing(event,x,y,flags,param):
    global objects
    if event==cv2.EVENT_LBUTTONDOWN:
        objects.append([x,y])

# getting direction of move from Q-Learning Model
def get_action(state):
    final_move = [0,0]
    state0 = torch.tensor(state, dtype=torch.float)
    prediction = model(state0)
    move = torch.argmax(prediction).item()
    final_move[move] = 1
    return final_move   

def get_command(bot, head, dest):
    global previous_angle

    left_speed = 0
    right_speed = 0

    max_speed = MAX_ABS_SPEED

    angle_threshold = (ANGLE_THRESHOLD_DEGREE*(math.pi))/180.0

    a = bot 
    b = head 
    c = dest 

    ab = sub(b,a)
    bc = sub(c,b) # this also can be ac

    angle = angle_between_points(ab, bc)
    ori = orientation(ab,bc)

    is_clockwise = int(ori == 1)

    state = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,is_clockwise]
    deg = angle * 180.0 / math.pi
    for i in range(18):
        if deg < (i+1) * 10:
            state[i] = 1
            break
    
    if(angle > angle_threshold):
        move = get_action(state)
        if move[0] == 1:            #cw
            left_speed = -ROTATION_CONST_SPEED
            right_speed = ROTATION_CONST_SPEED
        if move[1] == 1:            #ccw
            left_speed = ROTATION_CONST_SPEED
            right_speed = -ROTATION_CONST_SPEED
    else:
        abs_speed = max_speed*FORWARD_K*(distance(b,c)/200)
        left_speed = abs_speed
        right_speed = abs_speed
    
    #sanitizing the speed value wrt the allowed maximum speed globally
    left_speed = int(min(left_speed,max_speed))
    right_speed = int(min(right_speed,max_speed))

    left_speed = int(max(left_speed,-max_speed))
    right_speed = int(max(right_speed,-max_speed))

    return "spd " + str(left_speed) + " " + str(right_speed)


def video_thread():
    global objects
    global CONTROL_STATE
    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
    print('Video thread started')
    # Open a video capture object (0 for default camera, or specify the video file path)
    # cap = cv2.VideoCapture(1)
    cap = cv2.VideoCapture(1)

    cv2.setMouseCallback('Video',drawing)

    global is_connected

    command = ""
    frame_cnt = 0

    while True:
        print(CONTROL_STATE)
        # Capture frame-by-
        # frame
        ret, frame = cap.read()

        # Check if the frame is successfully captured
        if not ret:
            print("Failed to capture frame")
            break

        # Resize the frame to the desired display dimensions
        frame = cv2.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
        f = frame.copy()

        frame, bot, head, dest, path = process_image(frame)

        # if bot is None or head is None or dest is None:
            # continue
        # if CONTROL_STATE == "RESET":
        #     objects.clear()
        try:
            if CONTROL_STATE != "RESET" or 1==1:
                if len(objects) == 0 and distance(head, dest) > 50:
                    frame, bot, head, dest, path = process_image(f, True)
                    for i in range(1,len(path)):
                        objects.append((int(path[i][0]),int(path[i][1])))
        except:
            pass

        if len(objects) > 0:
            dest = objects[0]

        print("Dest = ", dest)

        # print(dx, dy)
        if is_connected and 1==1:
            if(frame_cnt == 0):
                if(bot is not None and head is not None and dest is not None):
                    if(distance(head, dest) < 50):
                        command = ""
                        #ws.send("")
                        if len(objects) > 0:
                            objects.remove(objects[0])
                    else:
                        command = get_command(bot, head, dest)
                        #ws.send(command)
                else:
                    #ws.send("")
                    command = ""
            
            ws.send(command)
        
        

        # Display the resulting frame

        # Draw the path in the image
        for i in range(len(objects)):
            cv2.circle(frame, [objects[i][0],objects[i][1]], 5, (0,0,255), -1)

        for i in range(len(objects)-1):
            cv2.circle(frame, [objects[i][0],objects[i][1]], 5, (0,255,0), -1)
            cv2.line(frame,[objects[i][0],objects[i][1]],[objects[i+1][0],objects[i+1][1]],(255,0,0),2)

        cv2.imshow('Video', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        frame_cnt = (frame_cnt + 1)%SKIP_FRAMES


    # Release the video capture object and close the window
    cap.release()
    cv2.destroyAllWindows()



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
# ui_thread = threading.Thread(target=run_ui)
# ui_thread.daemon = True
# ui_thread.start()


threading.Thread(target=video_thread).start()

ws.run_forever()