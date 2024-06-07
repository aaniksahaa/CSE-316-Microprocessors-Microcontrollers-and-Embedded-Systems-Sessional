import math
import cv2
import numpy as np
import heapq

UP = "w"
DOWN = "s"
RIGHT = "d"
LEFT = "a"

#HSV lower and upper thresholds

BOT = np.array([[0, 114, 92],[17, 254, 232]])
HEAD = np.array([[60, 113, 7],[90, 253, 147]])
DEST = np.array([[89, 158, 54],[119, 255, 194]])
OBS = np.array([[160, 17, 125],[190, 157, 255]])




# intersection


def line_intersects_rectangle(line_start, line_end, rectangle_center, rectangle_width, rectangle_height):
    # Unpack coordinates
    x1, y1 = line_start
    x2, y2 = line_end
    cx, cy = rectangle_center
    w = rectangle_width / 2
    h = rectangle_height / 2

    # Check if any point of the line segment is inside the rectangle
    if (min(x1, x2) <= cx + w and max(x1, x2) >= cx - w and
        min(y1, y2) <= cy + h and max(y1, y2) >= cy - h):
        return True

    # Check if any edge of the rectangle intersects the line segment
    edges = [((cx - w, cy - h), (cx + w, cy - h)),
             ((cx + w, cy - h), (cx + w, cy + h)),
             ((cx + w, cy + h), (cx - w, cy + h)),
             ((cx - w, cy + h), (cx - w, cy - h))]

    for edge_start, edge_end in edges:
        if line_segments_intersect(line_start, line_end, edge_start, edge_end):
            return True

    return False

def line_segments_intersect(p1, p2, p3, p4):
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - \
              (q[0] - p[0]) * (r[1] - q[1])

        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2

    o1 = orientation(p1, p2, p3)
    o2 = orientation(p1, p2, p4)
    o3 = orientation(p3, p4, p1)
    o4 = orientation(p3, p4, p2)

    if (o1 != o2 and o3 != o4):
        return True

    return False



#Dijkstra 



def euclidean_distance(p1, p2):
    # Calculate the Euclidean distance between two points
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

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




import random

def get_random_point(x_min, x_max, y_min, y_max):
    # Generate random x and y coordinates within the given range
    x = int(random.uniform(x_min, x_max))
    y = int(random.uniform(y_min, y_max))
    return x, y

#function to cheeck if point inside rectangle
def is_point_inside_rectangle(p, q, x, y, w, h):
    # Calculate the half-width and half-height of the rectangle
    half_w = w / 2
    half_h = h / 2

    # Calculate the bounds of the rectangle
    left_bound = x - half_w
    right_bound = x + half_w
    top_bound = y - half_h
    bottom_bound = y + half_h

    # Check if the point lies inside the bounds
    if left_bound <= p <= right_bound and top_bound <= q <= bottom_bound:
        return True
    else:
        return False

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


def draw_circle_around_point(image, center, radius=4, color=(0, 255, 0), thickness=-1):
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

def draw_bounding_box_with_offset(image, contour, color=(0, 255, 0), thickness=-1, offset=0):
    new_image = image.copy()  # Create a copy to avoid modifying the original image

    # Convert the contour to a bounding rectangle
    x, y, w, h = cv2.boundingRect(contour)

    # print(x, y, w, h)

    # Draw the bounding box on the image
    cv2.rectangle(new_image, (x-offset, y-offset), (x + w + offset, y + h + offset), color, thickness)

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

    if(bot_center and dest_center and head_center):
        image = draw_line_between_points(image, bot_center, dest_center)


    # generate random points now...

    points = []

    n_w = 10
    n_h = 6

    d_w = display_width // n_w
    d_h = display_height // n_h

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

    path = get_shortest_path_sequence(points, obstacles)

    print(path)

    for i in range(len(path)-1):
        image = draw_line_between_points(image, path[i], path[i+1], (0,0,255))

    return image, bot_center, head_center, dest_center


# Set the desired display dimensions
display_width = 1920
display_height = 1080


# Create a named window
cv2.namedWindow('scene', cv2.WINDOW_NORMAL)

# Resize the window
cv2.resizeWindow('scene', 1920, 1080)

IMAGE_PATH = 'images/a8.jpg'

image = cv2.imread(IMAGE_PATH)
frame = image 

# Resize the frame to the desired display dimensions
frame = cv2.resize(frame, (display_width, display_height))

frame, bot, head, dest = process_image(frame)

cv2.imshow('scene', frame)

cv2.waitKey(0)


