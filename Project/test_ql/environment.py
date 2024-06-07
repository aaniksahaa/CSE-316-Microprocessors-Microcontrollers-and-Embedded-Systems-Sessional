import math
import cv2
import numpy as np
from vector import *
from cv2_utils import *
import time

class Environment:
    def __init__(self):
        self.cap = cv2.VideoCapture(1)
        self.display_width = 1400
        self.display_height = 1000
        self.angle_threshold = (10*(math.pi))/180.0
        print("Camera is opened: ", self.cap.isOpened())
        # time.sleep(5)

    def get_reward(self):
        self.get_data()

        reward = 0
        done = False
        score = 0
        if self.angle < self.angle_threshold:
            score = 1
            reward = 10
            done = True
        else:
            score = 0
            reward = -self.reward
            done = False
        print(int(self.angle * 180/math.pi),self.reward)
        return reward, done, score

    def get_data(self):
        while True:    
            ret, frame = self.cap.read()
            frame = cv2.resize(frame, (self.display_width, self.display_height))
            frame, bot, head, dest = process_image(frame)
            if bot == None or head == None or dest == None:    
                continue
            else:
                self.bot = bot
                self.head = head
                self.dest = dest
                break

        a = self.bot 
        b = self.head 
        c = self.dest 

        ab = sub(b,a)
        bc = sub(c,a) # this also can be ac

        self.angle = angle_between_points(ab, bc)
        self.ori = orientation(ab,bc)
        
        self.is_clockwise = int(self.ori == 1)
        self.is_reached = int(distance(self.head, self.dest) < 50)


        state = [0,0,0,0,0,0,self.is_clockwise]
        deg = self.angle * 180.0 / math.pi
        for i in range(6):
            if deg < (i+1) * 30:
                state[i] = 1
                self.reward = 30 * (i+1)
                break
        self.state = state
        
        return bot, head, dest

    def get_state(self):
        self.get_data()
        return self.state
