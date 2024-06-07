import math

# Define two points as lists [x, y]
point1 = [0, 1]
point2 = [1, 1]

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

# Example usage
print("Distance between points:", distance(point1, point2))
print("Dot product of points:", dot(point1, point2))
print("Sum of points:", add(point1, point2))
print("Difference of points:", sub(point1, point2))


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

print(angle_between_points(point1, point2))



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
    
point1 = [-1,0]
point2 = [-1,1]

print(orientation(point1, point2))

