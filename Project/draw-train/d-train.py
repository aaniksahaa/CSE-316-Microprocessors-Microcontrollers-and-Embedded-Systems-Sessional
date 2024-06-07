import cv2
import numpy as np

# Global variables to store coordinates of the bounding box
bbox_start = None
bbox_end = None
drawing = False

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

# Load the image
image = cv2.imread('a2.jpg')

# Create a window and set the mouse callback function
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_bbox)

while True:
    img_copy = image.copy()

    if bbox_start and not drawing:
        cv2.rectangle(img_copy, bbox_start, bbox_end, (0, 255, 0), 2)

    cv2.imshow('image', img_copy)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        if bbox_start and bbox_end:
            x1, y1 = bbox_start
            x2, y2 = bbox_end
            bbox = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
            h_avg, s_avg, v_avg = calculate_hsv_avg(image, bbox)
            print("HSV Average (H, S, V):", h_avg, s_avg, v_avg)

cv2.destroyAllWindows()
