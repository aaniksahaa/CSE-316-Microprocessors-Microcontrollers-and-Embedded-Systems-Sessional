import pygame
import numpy as np
import random
import math

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define constants
NUM_ACTIONS = 8  # Number of possible actions (rotations)
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EPISODES = 1000

# Define the robot class
class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0  # Angle in radians
        self.rect = pygame.Rect(self.x, self.y, 50, 30)

    def rotate(self, angle_change):
        self.angle += angle_change
        self.angle %= 2 * math.pi

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)
        end_x = self.x + 30 * math.cos(self.angle)
        end_y = self.y + 30 * math.sin(self.angle)
        pygame.draw.line(screen, RED, (self.x + 25, self.y + 15), (end_x + 25, end_y + 15), 5)

# Define the Q-learning agent
class QLearningAgent:
    def __init__(self):
        self.q_table = np.zeros((NUM_ACTIONS,))

    def choose_action(self):
        return np.argmax(self.q_table)

    def update_q_table(self, action, reward):
        self.q_table[action] += LEARNING_RATE * (reward - self.q_table[action])

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("QLearning Robot")

# Initialize robot and destination
robot = Robot(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
destination = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))

# Initialize Q-learning agent
agent = QLearningAgent()

# Main loop
running = True
episode = 0
while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Choose action based on Q-table
    action = agent.choose_action()

    # Calculate the angle to rotate the robot towards the destination
    angle_to_destination = math.atan2(destination[1] - robot.y, destination[0] - robot.x)
    angle_diff = angle_to_destination - robot.angle

    # Update the Q-table based on the difference in angles
    agent.update_q_table(action, -abs(angle_diff))

    # Rotate the robot based on the chosen action
    robot.rotate((action - 3) * 0.1)

    # Draw robot and destination
    robot.draw(screen)
    pygame.draw.circle(screen, BLACK, destination, 10)

    # Update the display
    pygame.display.flip()

    # Update the episode count
    episode += 1

    # Check if episode limit is reached
    if episode >= EPISODES:
        running = False

# Quit Pygame
pygame.quit()
