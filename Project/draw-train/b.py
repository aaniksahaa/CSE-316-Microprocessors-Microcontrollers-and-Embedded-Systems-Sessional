import cv2
import numpy as np

# Function to get average HSV value of a region
def get_avg_hsv(image, bbox):
    x1, y1, x2, y2 = bbox
    roi = image[y1:y2, x1:x2]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    avg_hsv = np.mean(hsv_roi, axis=(0, 1))
    return avg_hsv

# Callback function for mouse events
def draw_bbox(event, x, y, flags, param):
    global drawing, bbox, img, original_img
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        bbox = [x, y, x, y]
    
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            bbox[2], bbox[3] = x, y
    
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        bbox[2], bbox[3] = x, y
        cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
        cv2.imshow('image', img)
        
        avg_hsv = get_avg_hsv(original_img, bbox)
        print("Average HSV:", avg_hsv)
        
        hsv_range = [(avg_hsv[0] - 20, avg_hsv[1] - 20, avg_hsv[2] - 20),
                     (avg_hsv[0] + 20, avg_hsv[1] + 20, avg_hsv[2] + 20)]
        
        # Create mask using HSV range
        lower = np.array([hsv_range[0][0], hsv_range[0][1], hsv_range[0][2]])
        upper = np.array([hsv_range[1][0], hsv_range[1][1], hsv_range[1][2]])
        mask = cv2.inRange(original_img, lower, upper)
        
        # Apply mask to create image
        masked_img = cv2.bitwise_and(original_img, original_img, mask=mask)
        
        # Draw bounding box on mask
        mask_with_bbox = cv2.rectangle(masked_img.copy(), (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
        
        # Display images
        cv2.imshow('Mask', mask_with_bbox)
        cv2.imshow('HSV Range Mask', masked_img)

# Read the image
img = cv2.imread('a2.jpg')
original_img = img.copy()

# Create a window and set the mouse callback function
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_bbox)

# Variables to track mouse events
drawing = False
bbox = [0, 0, 0, 0]

while True:
    cv2.imshow('image', img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
