import math
def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
def dot(p1, p2):
    return p1[0]*p2[0] + p1[1]*p2[1]
def add(p1, p2):
    return [p1[0] + p2[0], p1[1] + p2[1]]
def sub(p1, p2):
    return [p1[0] - p2[0], p1[1] - p2[1]]
def mul(p, x):
    return [p[0] * x, p[1] * x]

def magnitude(p):
    return math.sqrt(p[0]**2 + p[1]**2)
def angle_between_points(p1, p2):
    d = dot(p1, p2)
    mag_p1 = magnitude(p1)
    mag_p2 = magnitude(p2)
    if mag_p1 == 0 or mag_p2 == 0:
        return None
    cos_theta = d / (mag_p1 * mag_p2)
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
