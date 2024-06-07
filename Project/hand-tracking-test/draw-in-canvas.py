import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (255,0,0)

################################
wCam, hCam = 1600, 1200
################################



# Replace 'image_path.jpg' with the path to your local image
image_path = 'scene.jpg'

# Load the image
image = cv2.imread(image_path)

# Check if the image was loaded successfully
if image is not None:
    print("Image loaded successfully!")
else:
    print("Failed to load the image.")

canvas = np.full((wCam, hCam, 3), 255, dtype=np.uint8)
# orig_image = image 
# canvas = image 

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector()

drawing = False

px = 0
py = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    
    if len(lmList) != 0:
        lmList = lmList[0]  # the first instance of detected hand
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        #mirroring
        #x2 = wCam - x2
        
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        # cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        # cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        # cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        manahattan = abs(px-x2) + abs(py-y2)

        if(manahattan > 20 and (drawing == False or manahattan < 200)):

            col = ''
            if(drawing == False):
                col = WHITE
            else:
                col = BLACK

            cv2.circle(canvas, (px, py), radius=8, color=col, thickness=-1)  # Assuming RGB image, -1 for filled circle

            # Draw a black circle around the point (x, y)
            cv2.circle(canvas, (x2, y2), radius=8, color=BLUE, thickness=-1)  # Assuming RGB image, -1 for filled circle

            if(drawing):
                # Draw a black circle around the point (x, y)
                cv2.circle(canvas, (x2, y2), radius=4, color=BLACK, thickness=-1)  # Assuming RGB image, -1 for filled circle
                cv2.line(canvas, (px, py), (x2, y2), BLACK, thickness=4)
            px = x2 
            py = y2

    #canvas = cv2.flip(canvas, 1)

    # Display the updated image
    cv2.imshow('Canvas', canvas)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    #cv2.imshow("Img", img)

    key = cv2.waitKey(1)
    if key == 27:  # Press 'Esc' to exit the loop
        break
    elif key == ord('D') or key == ord('d'):
        print('D pressed')
        drawing = True
    elif key == ord('E') or key == ord('e'):
        print('E pressed')
        drawing = False
    elif key == ord('C') or key == ord('c'):
        print('C pressed')
        # clear drawings
        drawing = False
        canvas = np.full((wCam, hCam, 3), 255, dtype=np.uint8)