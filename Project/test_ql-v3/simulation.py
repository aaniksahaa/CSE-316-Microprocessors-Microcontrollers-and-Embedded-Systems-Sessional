import pygame
import math
import random
import time
from vector import *

class Box:
    def __init__(self, x=-1, y=-1, width=50, height=30, speed=5, angle=-1):
        if x == -1:
            x = random.randint(100, 500)
        if y == -1:
            y = random.randint(100, 500)
        if angle == -1:
            angle = random.randint(0, 90)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.speed = speed
        self.points = []
        self.generate_points()

    def get_direction(self):
        a = self.points[0]
        b = self.points[3]
        c = add(a,b)
        c = mul(c, 0.5)
        center = [self.x, self.y]
        return sub(c, center)        

    def get_angle(self):
        return self.angle * math.pi / 180.0
    
    def get_position(self):
        return [self.x, self.y]
    
    def generate_points(self):
        self.points = []
        radius = math.sqrt((self.height / 2)**2 + (self.width / 2)**2)
        angle = math.atan2(self.height / 2, self.width / 2)
        angles = [angle, -angle + math.pi, angle + math.pi, -angle]
        rot_radians = (math.pi / 180) * self.angle
        for angle in angles:
            y_offset = -1 * radius * math.sin(angle + rot_radians)
            x_offset = radius * math.cos(angle + rot_radians)
            self.points.append((self.x + x_offset, self.y + y_offset))

    def rotate(self, angle):
        self.angle += angle
        self.generate_points()

    def move_forward(self):
        self.x += 5 * math.cos(math.radians(self.angle))
        self.y -= 5 * math.sin(math.radians(self.angle))
        self.generate_points()

    def draw(self, screen):
        points = self.points
        pygame.draw.polygon(screen, 'red', self.points)
        pygame.draw.circle(screen, 'green', self.points[0], 3)
        pygame.draw.circle(screen, 'green', self.points[3], 3)

class Environment:
    def get_object(self, id):
        return self.objects[id]
        
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.objects = []
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('QL')
        self.reset_objects()

    def reset_objects(self):
        self.objects.clear()
        car = Box(300,300)
        dest = Box(500,100,angle=0)
        self.objects.append(car)
        self.objects.append(dest)
        
    def rotate_car(self, angle):
        self.objects[0].rotate(angle)

    def get_angle(self):
        car = self.objects[0].get_position()
        dest = self.objects[1].get_position()
        
        cd = sub(dest, car)
        dir = self.objects[0].get_direction()

        angle = angle_between_points(cd, dir) * 180 / math.pi

        ori = orientation(cd, dir)

        is_clockwise = 0
        if ori == -1:
            is_clockwise = 1

        return [angle, is_clockwise]
    
    def get_state(self):
        car = self.objects[0].get_position()
        dest = self.objects[1].get_position()
        
        cd = sub(dest, car)
        dir = self.objects[0].get_direction()

        angle = angle_between_points(cd, dir) * 180 / math.pi
        ori = orientation(cd, dir)

        is_clockwise = 0
        if ori == -1:
            is_clockwise = 1

        state = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,is_clockwise]
        deg  = angle

        for i in range(18):
            if deg < (i+1) * 10:
                state[i] = 1
                break
        return state

    def get_reward(self, old_state, new_state):
        reward = 0
        done = False
        score = 0
        p = 0
        q = 0
        for i in range(18):
            if old_state[i] == 1:
                p = i
            if new_state[i] == 1:
                q = i
        if q < p:
            reward = 1
        else:
            reward = -1

        if new_state[0] == 1:
            done = True
        else:
            done = False
        # print(int(self.angle * 180/math.pi),self.reward)
        return reward, done, score
            
    def draw(self):
        self.screen.fill('white')
        for object in self.objects:
            object.draw(self.screen)

        car = self.objects[0].get_position()
        car_angle = self.objects[0].get_angle()

        dest = self.objects[1].get_position()
        car2 = [car[0] + 100 * math.cos(car_angle), car[1] - 100 * math.sin(car_angle)]
        pygame.draw.line(self.screen,'green', car, car2, 2)
        angle = math.atan2(dest[1]-car[1],dest[0]-car[0])
        pygame.draw.line(self.screen,'black',car,dest,2)
        pygame.display.flip()
        self.clock.tick(30)

# running = True
# env = Environment()

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     keys = pygame.key.get_pressed()

#     if keys[pygame.K_a]:
#         env.rotate_car(5)
#     if keys[pygame.K_d]:
#         env.rotate_car(-5)
#     env.draw()
#     env.get_state()
#     print(env.get_state())

# pygame.quit()