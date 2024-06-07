import pygame
import sys
from vector import *
from line_rect_int import *

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Draw Rectangles and Lines")

# Variables to store drawing information
drawing_rect = False
rect_start = (0, 0)
rect_end = (0, 0)
drawing_line = False
line_start = (0, 0)
line_end = (0, 0)

rects = []
lines = []
# Main game loop
while True:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if not drawing_rect:
                    rect_start = event.pos
                    drawing_rect = True
            elif event.button == 3:
                if not drawing_line:
                    line_start = event.pos
                    drawing_line = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if drawing_rect:
                    rect_end = event.pos
                    drawing_rect = False
                    rects.append([rect_start, rect_end])

            if event.button == 3:
                if drawing_line:
                    line_end = event.pos
                    drawing_line = False
                    lines.append([line_start, line_end])
                    for i in range(len(rects)):
                        center = add(rects[i][0], rects[i][1])
                        center = mul(center, 0.5)
                        d = sub(rects[i][0], rects[i][1])
                        w = abs(d[0])
                        h = abs(d[1])
                        j = line_intersects_rectangle(line_start,line_end,center,w,h)
                        if j:
                            print(i)

    for line in lines:
        pygame.draw.line(screen, BLACK, line[0], line[1], 2)
    for rect in rects:
        pygame.draw.rect(screen, BLACK, (rect[0][0], rect[0][1], rect[1][0]-rect[0][0], rect[1][1]-rect[0][1]), 2)
        
    # Drawing
    if drawing_rect:
        pygame.draw.rect(screen, BLACK, (rect_start[0], rect_start[1],
                                          pygame.mouse.get_pos()[0] - rect_start[0],
                                          pygame.mouse.get_pos()[1] - rect_start[1]), 2)

    if drawing_line:
        pygame.draw.line(screen, BLACK, line_start, pygame.mouse.get_pos(), 2)

    # Update the display
    pygame.display.flip()
