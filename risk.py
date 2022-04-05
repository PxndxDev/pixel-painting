import pygame
import time
import random

width = 500
height = 500
buttons = 50

points = [[i, (255, 0, 0) if i%2==1 else (0, 0, 255), [500 / buttons * i, random.randint(0, 500 / buttons * i)]] for i in range(buttons)]

pygame.init()

screen = pygame.display.set_mode((width, height))

dist = lambda x1,x2,y1,y2: ((x1-x2)**2 + (y1-y2)**2)**0.5
widthScale = width // 60
heightScale = height // 60
circleRadius = 4

def draw(k):
    x = circleRadius
    y = circleRadius
    drawing = True
    screen.fill((150, 150, 150))
    while drawing:
        nearPoints = sorted(points, key = lambda pt: dist(pt[2][0], x, pt[2][1], y))

        if nearPoints.__len__() < k:
            if nearPoints.__len__() == 0:
                nearPoints = nearPoints[0]
        else:
            nearPoints = nearPoints[0:k]
        
        colors = [list(filter(lambda pt: pt[1] == (255, 0, 0), nearPoints)), list(filter(lambda pt: pt[1] == (0, 0, 255), nearPoints))]
        color = (255, 0, 0) if colors[0].__len__() > colors[1].__len__() else (0, 0, 255)

        pygame.draw.circle(screen, color, (x, y), circleRadius)

        x += widthScale
        if x >= width - circleRadius * 2:
            x = circleRadius
            y += widthScale
        elif y >= height - circleRadius * 2:
            drawing = False

        pygame.display.update()
    
    for pt in points:
        pygame.draw.circle(screen, pt[1], (pt[2][0], pt[2][1]), circleRadius * 5)
        pygame.draw.circle(screen, (255, 255, 255), (pt[2][0], pt[2][1]), circleRadius * 5, 3)
        pygame.display.update()

mode = 0
pts = []
K = 3

draw(K)

playing = True
while playing:
    collidings = list(filter(lambda pt: pygame.Rect(pt[2][0] - circleRadius * 5, pt[2][1] - circleRadius * 5, circleRadius * 10, circleRadius * 10).collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), points))
    if mode == 1:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
    elif mode == 0:
        if collidings.__len__() > 0:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if mode == 0:
                    if collidings.__len__() > 0:
                        pts = collidings[0]
                        mode = 1
                elif mode == 1:
                    points = list(filter(lambda pt: pt[0] != pts[0], points))
                    pts[2] = [event.pos[0], event.pos[1]]
                    points.append(pts)
                    draw(K)
                    mode = 0
                
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_KP_PLUS, pygame.K_KP_MINUS]:
                if event.key == pygame.K_KP_PLUS:
                    K += 2
                elif event.key == pygame.K_KP_MINUS:
                    K -= 2
                if K < 1:
                    K = 1
                if K > 9:
                    K = 9
                
                print("touche pressé, K=", K)
                draw(K)
            elif event.key == pygame.K_ESCAPE:
                playing = False
                pygame.quit()