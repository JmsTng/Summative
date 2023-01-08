### IMPORTS ###
import os
import sys

import pygame
from objects import Player, Object


### CONSTANTS ###
pygame.init()

# COLOURS
black = (0, 0, 0)
white = (255, 255, 255)

# DISPLAY
screen = pygame.display.set_mode()
size = width, height = screen.get_size()
center = (width//2, height//2)

# OBJECTS
walls = [
    Object(canvas=screen, x=-1, y=-1, w=2, h=height), # left
    Object(canvas=screen, x=width-1, y=-1, w=2, h=height+2), # right
    Object(canvas=screen, x=-1, y=-1, w=width+2, h=2), # top
    Object(canvas=screen, x=-1, y=height-1, w=width+2, h=2)]

speed = width//1000
P1 = Player(
    canvas=screen,
    path=os.path.join("assets", "Character1.png"),
    keys=(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d),
    speed=speed,
    x=center[0]-32,
    y=center[1],
    img_scale=2
)
P2 = Player(
    canvas=screen,
    path=os.path.join("assets", "Character2.png"),
    keys=(pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT),
    speed=speed,
    x=center[0]+32,
    y=center[1],
    img_scale=2
)

box = Object(canvas=screen, path=r'assets\Stone1.png', x=400, y=123, img_scale=3)

# INTERACTION
pygame.key.set_repeat(5*speed)


### EVENT LOOP ###
while True:
    screen.fill(black)
    pygame.event.pump()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_r:
                    P1.rect.x, P1.rect.y = center[0]-32, center[1]
                    P2.rect.x, P2.rect.y = center[0]+32, center[1]
        
    if any(pressed := pygame.key.get_pressed()):
        keys = ['']*8
        for key in P1.keys+P2.keys:
            if pressed[key]:
                keys.append(key)
        P1.move((P2,*walls, box), keys)
        P2.move((P1,*walls), keys)

    P1.render(screen)
    P2.render(screen)
    for wall in walls:
        wall.render(color=white, solid=True)
    box.render()

    pygame.display.flip()
