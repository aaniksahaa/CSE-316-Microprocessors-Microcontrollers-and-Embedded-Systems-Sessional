import numpy as np

UP = "w"
DOWN = "s"
RIGHT = "d"
LEFT = "a"

#define colors 

RED = [[0,173,150],[35,255,255]]
GREEN = [[50,97,32],[92,255,255]]
BLUE = [[84,138,32],[108,255,255]]
PINK = [[166,89,157],[179,110,182]]
YELLOW = None

#HSV lower and upper thresholds

BOT = np.array(RED)
HEAD = np.array(GREEN)
DEST = np.array(BLUE)
OBS = np.array(PINK)

# hyperparameters for speed control 

MAX_ABS_SPEED = 160
ROTATION_CONST_SPEED = 100

# proportional constants

FORWARD_K = 15
ROTATION_K = 1.5 # not used in case of RL

#threshold values 

ANGLE_THRESHOLD_DEGREE = 30
DETECTION_DEVIATION_THRESHOLD = 1

# global settings

DISPLAY_WIDTH = 1920
DISPLAY_HEIGHT = 1080

# Network Settings

IP = "192.168.137.84"
PORT = "81"

# Customization

SKIP_FRAMES = 2