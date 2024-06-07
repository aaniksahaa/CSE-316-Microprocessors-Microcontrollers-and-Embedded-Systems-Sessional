import cv2
import numpy as np

# Global variables to store coordinates of the bounding box
bbox_start = None
bbox_end = None
drawing = False


def draw_line_between_points(image, start_point, end_point, color=(0, 255, 0), thickness=2):
    new_image = image.copy()  # Create a copy to avoid modifying the original image
    start_point = tuple(map(int, start_point))  # Ensure start point coordinates are integers
    end_point = tuple(map(int, end_point))  # Ensure end point coordinates are integers

    # Draw the line on the image
    cv2.line(new_image, start_point, end_point, color, thickness)

    return new_image


def draw_circle_around_point(image, center, radius=10, color=(0, 255, 0), thickness=-1):
    new_image = image.copy()  # Create a copy to avoid modifying the original image
    center = tuple(map(int, center))  # Ensure center coordinates are integers

    # Draw the circle on the image
    cv2.circle(new_image, center, radius, color, thickness)

    return new_image

# Function to draw the bounding box
def draw_bbox(event, x, y, flags, param):
    global bbox_start, bbox_end, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        bbox_start = (x, y)
        drawing = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            bbox_end = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        bbox_end = (x, y)
        drawing = False

# Function to calculate HSV average
def calculate_hsv_avg(image, bbox):
    x1, y1, x2, y2 = bbox
    roi = image[y1:y2, x1:x2]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    h_avg = np.mean(hsv_roi[:,:,0])
    s_avg = np.mean(hsv_roi[:,:,1])
    v_avg = np.mean(hsv_roi[:,:,2])
    return (h_avg, s_avg, v_avg)



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



def draw_bounding_box_from_hsv(image, lower,upper):
    red_contours, red_centers = get_detected_object_centers(image, lower, upper, 1)

    bot_center = None

    if(len(red_centers) > 0):
        image = draw_bounding_box(image, red_contours[0])
        bot_center = red_centers[0]
    else:
        print('Bot out of view')
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


# Load the image

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
ret = 1
frame = 1
for i in range(100):
    ret, frame = cap.read()

# image = cv2.imread(IMAGE_PATH)
image = frame


# Set the desired display dimensions
display_width = 1920
display_height = 1080

image = cv2.resize(image, (display_width, display_height))

# Create a window and set the mouse callback function
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image', draw_bbox)

cv2.resizeWindow('image', 1920, 1080)

orig_image = image
def get_array(x):
    r = "[" + str(x[0]) + "," + str(x[1]) + "," + str(x[2]) + "]"
    return r

while True:
    #img_copy = orig_image.copy()

    img_copy = orig_image.copy()

    if bbox_start and not drawing:
        cv2.rectangle(img_copy, bbox_start, bbox_end, (0, 255, 0), 2)

    cv2.imshow('image', img_copy)
    #cv2.namedWindow('hehe')

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        if bbox_start and bbox_end:
            x1, y1 = bbox_start
            x2, y2 = bbox_end
            bbox = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
            image = orig_image
            h_avg, s_avg, v_avg = calculate_hsv_avg(image, bbox)
            print("HSV Average (H, S, V):", h_avg, s_avg, v_avg)
            mask = [h_avg, s_avg, v_avg]
            diffs = [10,20,20]
            lower = np.array([int(max(0, mask[x] - diffs[x])) for x in range(0,3)])
            upper = np.array([int(min(255,mask[x] + diffs[x])) for x in range(0,3)])
            print("[" + get_array(lower) + "," + get_array(upper) + "]")
            image = draw_bounding_box_from_hsv(image, lower, upper)
            cv2.imshow('hehe',image)
            key = cv2.waitKey(2)
cv2.destroyAllWindows()
