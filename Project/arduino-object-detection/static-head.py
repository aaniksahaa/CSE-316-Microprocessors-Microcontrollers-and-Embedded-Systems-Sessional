import math
import cv2
import numpy as np

UP = "w"
DOWN = "s"
RIGHT = "d"
LEFT = "a"





# Function to calculate distance between two points
def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

# Function to calculate dot product of two points
def dot(p1, p2):
    return p1[0]*p2[0] + p1[1]*p2[1]

# Function to add two points
def add(p1, p2):
    return [p1[0] + p2[0], p1[1] + p2[1]]

# Function to subtract two points
def sub(p1, p2):
    return [p1[0] - p2[0], p1[1] - p2[1]]

def magnitude(p):
    return math.sqrt(p[0]**2 + p[1]**2)

# Function to calculate the angle (in radians) between two points
def angle_between_points(p1, p2):
    d = dot(p1, p2)
    mag_p1 = magnitude(p1)
    mag_p2 = magnitude(p2)

    # Avoid division by zero
    if mag_p1 == 0 or mag_p2 == 0:
        return None

    cos_theta = d / (mag_p1 * mag_p2)
    # Calculate angle in radians
    angle_rad = math.acos(cos_theta)
    return angle_rad


def cross_product(p1, p2):
    return p1[0] * p2[1] - p1[1] * p2[0]

def orientation(p1, p2):
    result = cross_product(p1, p2)

    if result > 0:
        return 1    # ccw - turn left
    elif result < 0:
        return -1   # cw  - turn right
    else:
        return 0
    

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


def draw_circle_around_point(image, center, radius=10, color=(0, 255, 0), thickness=-1):
    new_image = image.copy()  # Create a copy to avoid modifying the original image
    center = tuple(map(int, center))  # Ensure center coordinates are integers

    # Draw the circle on the image
    cv2.circle(new_image, center, radius, color, thickness)

    return new_image

def draw_line_between_points(image, start_point, end_point, color=(0, 255, 0), thickness=2):
    new_image = image.copy()  # Create a copy to avoid modifying the original image
    start_point = tuple(map(int, start_point))  # Ensure start point coordinates are integers
    end_point = tuple(map(int, end_point))  # Ensure end point coordinates are integers

    # Draw the line on the image
    cv2.line(new_image, start_point, end_point, color, thickness)

    return new_image

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

def process_image_2(image):
    # Define red color range in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    red_contours, red_centers = get_detected_object_centers(image, lower_red, upper_red, 1)

    bot_center = None

    if(len(red_centers) > 0):
        image = draw_bounding_box(image, red_contours[0])
        for point in red_contours[0]:
            #print(point[0])
            image = draw_circle_around_point(image, point[0])
        bot_center = red_centers[0]
        #print(bot_center)
        #print(find_mean_point(red_contours[0]))
        image = draw_circle_around_point(image, bot_center)
    
    return image

def process_image(image):
    # Define red color range in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    red_contours, red_centers = get_detected_object_centers(image, lower_red, upper_red, 1)

    bot_center = None

    if(len(red_centers) > 0):
        image = draw_bounding_box(image, red_contours[0])
        bot_center = red_centers[0]
    else:
        print('Bot out of view')

    # Define blue color range in HSV
    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([130, 255, 255])

    blue_contours, blue_centers = get_detected_object_centers(image, lower_blue, upper_blue, 1)

    dest_center = None

    if(len(blue_centers) > 0):
        dest_center = blue_centers[0]
        image = draw_bounding_box(image, blue_contours[0])
    else:
        print('Destination out of view')


    # Define green color range in HSV
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])

    green_contours, green_centers = get_detected_object_centers(image, lower_green, upper_green, 1)

    head_center = None

    if(len(green_centers) > 0):
        image = draw_bounding_box(image, green_contours[0])
        head_center = green_centers[0]
    else:
        print('Head out of view')

    if(bot_center):
        image = draw_circle_around_point(image, bot_center)
    if(head_center):
        image = draw_circle_around_point(image, head_center, 10, (255,0,0))
    if(dest_center):
        image = draw_circle_around_point(image, dest_center)
    if(bot_center and dest_center and head_center):
        image = draw_line_between_points(image, bot_center, dest_center)

    return image, bot_center, head_center, dest_center

rotation_k = 1.5
forward_k = 15
previous_angle = 0
rotation_d = 0

def get_command(bot, head, dest):
    global rotation_k, forward_k, previous_angle

    left_speed = 0
    right_speed = 0

    max_speed = 250

    angle_threshold = (20*(math.pi))/180.0

    a = bot 
    b = head 
    c = dest 

    ab = sub(b,a)
    bc = sub(c,b) # this also can be ac

    dot_value = dot(ab,bc)
    angle = angle_between_points(ab, bc)
    ori = orientation(ab,bc)

    signed_angle = ori * angle
    

    if(angle > angle_threshold):
        abs_speed = max_speed*rotation_k*(angle/(math.pi)) + max_speed*(signed_angle - previous_angle)/math.pi * rotation_d
        previous_angle = signed_angle
        if(ori == 1):   # ccw
            left_speed = abs_speed
            right_speed = -abs_speed
        elif(ori == -1): # cw
            left_speed = -abs_speed
            right_speed = abs_speed
    else:
        abs_speed = max_speed*forward_k*(distance(b,c)/200)
        left_speed = abs_speed
        right_speed = abs_speed
    
    left_speed = int(min(left_speed,max_speed))
    right_speed = int(min(right_speed,max_speed))
    
    return "spd " + str(left_speed) + " " + str(right_speed)

# image = cv2.imread('images/test.jpg')
# image, bot, head, dest = process_image(image)
# print(get_command(bot, head, dest))

# # Display the result
# cv2.imshow('Result', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



# Set the desired display dimensions
display_width = 1400
display_height = 1000

import websocket

is_connected = False

# Define the WebSocket server address
server_address = "ws://192.168.137.194:81/"

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

ws = websocket.WebSocketApp(server_address,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
objects = []

def drawing(event,x,y,flags,param):
    global objects
    if event==cv2.EVENT_LBUTTONDOWN:
        objects.append([x,y])

def video_thread():
    global objects
    cv2.namedWindow('Video')
    print('Video thread started')
    # Open a video capture object (0 for default camera, or specify the video file path)
    # cap = cv2.VideoCapture(1)
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

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
        frame = cv2.resize(frame, (display_width, display_height))

        frame, bot, head, dest = process_image(frame)

        if len(objects) > 0:
            dest = objects[0]



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

import threading
threading.Thread(target=video_thread).start()

ws.run_forever()