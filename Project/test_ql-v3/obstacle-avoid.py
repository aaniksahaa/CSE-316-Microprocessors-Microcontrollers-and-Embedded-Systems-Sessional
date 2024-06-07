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

UP = "w"
DOWN = "s"
RIGHT = "d"
LEFT = "a"

#define colors 

RED = np.array([[0,109,202],[255,196,255]])
GREEN = np.array([[0,133,93],[86,255,158]])
BLUE = np.array([[89, 158, 54],[119, 255, 194]])
PINK = np.array([[0,33,197],[255,82,255]])
YELLOW = None

#HSV lower and upper thresholds

BOT = RED
HEAD = GREEN
DEST = BLUE
OBS = PINK


#define hyperparameters for speed control 

MAX_ABS_SPEED = 160
ROTATION_CONST_SPEED = 100

FORWARD_K = 15
ROTATION_K = 1.5 # not used in case of RL

#threshold values 

ANGLE_THRESHOLD_DEGREE = 30

# global settings

DISPLAY_WIDTH = 1920
DISPLAY_HEIGHT = 1080

# Network Settings

IP = "192.168.137.84"
PORT = "81"

# Reinforcement Learning Model

model = Linear_QNet(19, 256, 2)
model.load_state_dict(torch.load('model/model-100.pth'))
model.eval()

# Websocket Connection

is_connected = False

# Define the WebSocket server address
server_address = "ws://" + IP + ":" + PORT + "/"

# Define the callback function to handle WebSocket events
def on_message(ws, message):
    pass

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("WebSocket connection closed")


def on_open(ws):
    global is_connected
    is_connected = True
    print("WebSocket connection established")

# Helper functions

#Dijkstra 
def dijkstra_shortest_path(graph, start, end):
    # Initialize distances with infinity for all nodes except the start node
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    parent = {node: None for node in graph}
    
    # Priority queue to store nodes with their tentative distances
    priority_queue = [(0, start)]
    
    while priority_queue:
        # Pop the node with the smallest tentative distance
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # If reached the destination, return the shortest path
        if current_node == end:
            path = []
            while current_node is not None:
                path.insert(0, current_node)
                current_node = parent[current_node]
            return path
        
        # Check neighbors of the current node
        for neighbor in graph[current_node]:
            distance = current_distance + graph[current_node][neighbor]
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parent[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    # If no path found, return an empty list
    return []

def get_shortest_path_sequence(points, obstacles):
    # Create a graph where keys are integer indices and values are dictionaries of neighbors and distances
    n = len(points)
    graph = {i: {} for i in range(n)}
    for i in range(n):
        for j in range(n):
            if i != j:
                distance = euclidean_distance(points[i], points[j])
                graph[i][j] = distance
                ok = True
                for ob in obstacles:
                    x,y,w,h = ob
                    if(line_intersects_rectangle(points[i], points[j], [x,y], w, h)):
                        ok = False
                        break
                if(not ok):
                    graph[i][j] = 10000
    
    # Find the shortest path using Dijkstra's algorithm
    shortest_path_indices = dijkstra_shortest_path(graph, 0, n - 1)
    
    # Convert indices to points
    shortest_path_points = [points[i] for i in shortest_path_indices]
    
    return shortest_path_points


    

def find_mean_point(contour):
    num_points = len(contour)
    mean_x = sum(point[0][0] for point in contour) / num_points
    mean_y = sum(point[0][1] for point in contour) / num_points

    return (mean_x, mean_y)

def get_min_deviation(contour, center):
    dx = 0
    dy = 0
    for point in contour:
        p = point[0]
        dx += abs(p[0]-center[0])
        dy += abs(p[1]-center[1])
    return dx + dy


def get_detected_object_centers(image, lower_color, upper_color, max_objects=1, threshold = 100):
    # Convert to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Threshold the image
    red_mask = cv2.inRange(hsv_image, lower_color, upper_color)

    # Find contours in the binary mask
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    candidates = []

    # Iterate over contours
    for contour in contours:
        center = find_mean_point(contour)
        mean_deviation = get_min_deviation(contour, center)
        candidates.append([contour, center, mean_deviation])

    sorted_candidates = sorted(candidates, key=lambda x: x[2], reverse=True)

    detected_objects = sorted_candidates[:max_objects]

    object_contours = []
    object_centers = []

    for object in detected_objects:
        if(object[2] >= threshold):
            object_contours.append(object[0])
            object_centers.append(object[1])
    
    return object_contours, object_centers

def draw_bounding_box(image, contour, color=(0, 255, 0), thickness=-1):
    new_image = image.copy()  # Create a copy to avoid modifying the original image

    # Convert the contour to a bounding rectangle
    x, y, w, h = cv2.boundingRect(contour)

    # print(x, y, w, h)

    # Draw the bounding box on the image
    cv2.rectangle(new_image, (x, y), (x + w, y + h), color, thickness)

    return new_image

def draw_bounding_box_with_offset(image, contour, color=(0, 255, 0), thickness=-1, offset=0):
    new_image = image.copy()  # Create a copy to avoid modifying the original image

    # Convert the contour to a bounding rectangle
    x, y, w, h = cv2.boundingRect(contour)

    # print(x, y, w, h)

    # Draw the bounding box on the image
    cv2.rectangle(new_image, (x-offset, y-offset), (x + w + offset, y + h + offset), color, thickness)

    return new_image

# global list for holding the path sequence
path = []

def process_image(image, calc_path = False):
    bot_width = 50

    bot_contours, bot_centers = get_detected_object_centers(image, BOT[0], BOT[1], 1)
    bot_center = None 

    if(len(bot_centers) > 0):
        x, y, w, h = cv2.boundingRect(bot_contours[0])
        bot_width = w
        image = draw_bounding_box(image, bot_contours[0], (0,0,255))
        bot_center = bot_centers[0]
    else:
        print('Bot out of view')

    dest_contours, dest_centers = get_detected_object_centers(image, DEST[0], DEST[1], 1)
    dest_center = None

    if(len(dest_centers) > 0):
        dest_center = dest_centers[0]
        image = draw_bounding_box(image, dest_contours[0], (255,0,0))
    else:
        print('Destination out of view')


    head_contours, head_centers = get_detected_object_centers(image, HEAD[0], HEAD[1], 1)
    head_center = None

    if(len(head_centers) > 0):
        image = draw_bounding_box(image, head_contours[0], (15, 105, 18))
        head_center = head_centers[0]
    else:
        print('Head out of view')

    obs_contours, obs_centers = get_detected_object_centers(image, OBS[0], OBS[1], 6)
    obs_center = None
    obstacles = []
    num_obs = len(obs_centers)
    for i in range(num_obs):
        image = draw_bounding_box(image, obs_contours[i], (96, 12, 102))
        offset = int(bot_width/2) + 5
        image = draw_bounding_box_with_offset(image, obs_contours[i], (96, 12, 102), 2, offset)
        x, y, w, h = cv2.boundingRect(obs_contours[i])
        x += int(w/2)
        y += int(h/2)
        w += 2*offset
        h += 2*offset
        obstacles.append([x,y,w,h])
    print(obstacles)

    if calc_path:
        global path
        global objects
        if(bot_center and dest_center and head_center):
            image = draw_line_between_points(image, bot_center, dest_center)
        else:
            print(bot_center, dest_center, head_center)

        # generate random points now...

        points = []

        n_w = 10
        n_h = 6

        d_w = DISPLAY_WIDTH // n_w
        d_h = DISPLAY_HEIGHT // n_h

        for i in range(n_w):
            x = d_w//2 + d_w*i
            for j in range(n_h):
                y = d_h//2 + d_h*j
                ok = True
                for ob in obstacles:
                    if(is_point_inside_rectangle(x,y,ob[0],ob[1],ob[2],ob[3])):
                        ok = False
                        break
                if(ok):
                    points.append([x,y])
                    image = draw_circle_around_point(image, (x,y), 6, (255, 255, 255))

        points.insert(0,bot_center)
        points.append(dest_center)

        path = []
        try:
            path = get_shortest_path_sequence(points, obstacles)
            for i in range(1,len(path)):
                objects.append((int(path[i][0]),int(path[i][1])))
            # for i in range(len(path)-1):
                # image = draw_line_between_points(image, path[i], path[i+1], (0,0,255))
        except:
            print("error")
    return image, bot_center, head_center, dest_center


# Enable the Websocket Connection
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


rotation_k = ROTATION_K
forward_k = FORWARD_K
previous_angle = 0
rotation_d = 0


# getting direction of move from Q-Learning Model
def get_action(state):
    final_move = [0,0]
    state0 = torch.tensor(state, dtype=torch.float)
    prediction = model(state0)
    move = torch.argmax(prediction).item()
    final_move[move] = 1
    return final_move   

def get_command(bot, head, dest):
    global rotation_k, forward_k, previous_angle

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
        abs_speed = max_speed*forward_k*(distance(b,c)/200)
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
    skip_frames = 2

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

        frame, bot, head, dest = process_image(frame)

        # if bot is None or head is None or dest is None:
            # continue

        try:
            if len(objects) == 0 and distance(head, dest) > 50:
                frame, bot, head, dest = process_image(f, True)
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
                
        for i in range(len(objects)):
            cv2.circle(frame, [objects[i][0],objects[i][1]], 5, (0,0,255), -1)

        for i in range(len(objects)-1):
            cv2.circle(frame, [objects[i][0],objects[i][1]], 5, (0,255,0), -1)
            cv2.line(frame,[objects[i][0],objects[i][1]],[objects[i+1][0],objects[i+1][1]],(255,0,0),2)

        cv2.imshow('Video', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        frame_cnt = (frame_cnt + 1)%skip_frames


    # Release the video capture object and close the window
    cap.release()
    cv2.destroyAllWindows()


threading.Thread(target=video_thread).start()

ws.run_forever()


