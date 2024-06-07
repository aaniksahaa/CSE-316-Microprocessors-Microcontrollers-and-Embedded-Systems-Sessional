import cv2
import numpy as np 

objects = []

def drawing(event,x,y,flags,param):
    global objects
    if event==cv2.EVENT_LBUTTONDOWN:
        objects.append([x,y])

def video_thread():
    global objects
    cv2.namedWindow('Video')
    print('Video thread started')
    # Open a video capture object (0 for default camera, or specify the video file path)
    cap = cv2.VideoCapture(0)
    cv2.setMouseCallback('Video',drawing)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break
        frame = cv2.resize(frame, (1400, 1000))

        for x in objects:
            cv2.circle(frame, [x[0],x[1]], 5, (0,255,0), -1)

        cv2.imshow('Video', frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

import threading
threading.Thread(target=video_thread).start()

