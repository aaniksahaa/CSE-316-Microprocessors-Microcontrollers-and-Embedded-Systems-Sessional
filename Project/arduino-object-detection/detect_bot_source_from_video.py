import cv2
import numpy as np

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

def draw_bounding_box(image, contour, color=(0, 255, 0), thickness=-1):
    new_image = image.copy()  # Create a copy to avoid modifying the original image

    # Convert the contour to a bounding rectangle
    x, y, w, h = cv2.boundingRect(contour)

    print(x, y, w, h)

    # Draw the bounding box on the image
    cv2.rectangle(new_image, (x, y), (x + w, y + h), color, thickness)

    return new_image

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
        candidates.append([center, mean_deviation])

    sorted_candidates = sorted(candidates, key=lambda x: x[1], reverse=True)

    detected_objects = sorted_candidates[:max_objects]

    centers = []

    for object in detected_objects:
        if(object[1] >= threshold):
            centers.append(object[0])
    
    return centers

def process_image(image):
    # Define red color range in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    red_centers = get_detected_object_centers(image, lower_red, upper_red, 1)

    bot_center = None

    if(len(red_centers) > 0):
        bot_center = red_centers[0]
    else:
        print('Bot out of view')

    # Define blue color range in HSV
    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([130, 255, 255])

    blue_centers = get_detected_object_centers(image, lower_blue, upper_blue, 1)

    dest_center = None

    if(len(blue_centers) > 0):
        dest_center = blue_centers[0]
    else:
        print('Destination out of view')

    if(bot_center):
        image = draw_circle_around_point(image, bot_center)
    if(dest_center):
        image = draw_circle_around_point(image, dest_center)
    if(bot_center and dest_center):
        image = draw_line_between_points(image, bot_center, dest_center)

    return image

def process_image_2(image):
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

    if(bot_center):
        image = draw_circle_around_point(image, bot_center)
    if(dest_center):
        image = draw_circle_around_point(image, dest_center)
    if(bot_center and dest_center):
        image = draw_line_between_points(image, bot_center, dest_center)

    return image

# Set the desired display dimensions
display_width = 1400
display_height = 1000

# Open a video capture object (0 for default camera, or specify the video file path)
cap = cv2.VideoCapture(1)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if the frame is successfully captured
    if not ret:
        print("Failed to capture frame")
        break

    # Resize the frame to the desired display dimensions
    frame = cv2.resize(frame, (display_width, display_height))

    frame = process_image(frame)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()
