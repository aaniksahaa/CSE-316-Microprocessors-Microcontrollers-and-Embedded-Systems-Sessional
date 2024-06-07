import math
import cv2
import numpy as np
import heapq
import random
import websocket
import threading
from model import Linear_QNet, QTrainer
import torch

from util import *
from settings import *

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
        # Capture frame-by-frame
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

        try:
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
        if is_connected:
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


threading.Thread(target=video_thread).start()

ws.run_forever()


