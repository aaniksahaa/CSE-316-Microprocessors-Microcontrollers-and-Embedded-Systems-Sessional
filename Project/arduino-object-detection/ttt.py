import math

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

# Function to calculate distance between two points
def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

points = [[0,0], [1,1], [0,2], [4,0], [2,4]]

