import math 
import random 
import cv2 

# Geometry Utilities

#function to cheeck if a point lies inside a rectangle
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

def euclidean_distance(p1, p2):
    # Calculate the Euclidean distance between two points
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def get_random_point(x_min, x_max, y_min, y_max):
    # Generate random x and y coordinates within the given range
    x = int(random.uniform(x_min, x_max))
    y = int(random.uniform(y_min, y_max))
    return x, y


# Vector Utilities

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
    

# Drawing Utilities
    
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