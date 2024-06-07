import cv2
import numpy as np

# Start capturing video from the default camera (0)
cap = cv2.VideoCapture(1)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()

    b,g,r = cv2.split(frame)
    rg = r - g
    rb = r - b
    rg = np.clip(rg, 0, 255)
    rb = np.clip(rb, 0, 255)

    mask1 = cv2.inRange(rg, 50, 255)
    mask2 = cv2.inRange(rb, 50, 255)
    mask = cv2.bitwise_and(mask1, mask2)

    cv2.imshow('Original Frame', frame)
    cv2.imshow('Red Detected', mask)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
