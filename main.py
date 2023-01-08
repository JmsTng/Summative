### IMPORTS ###
import os
import sys

import pygame
from objects import Player


### CONSTANTS ###
pygame.init()

# COLOURS
black = (0, 0, 0)
white = (255, 255, 255)

# DISPLAY
screen = pygame.display.set_mode()
size = width, height = screen.get_size()
center = (width//2, height//2)
print(size)

# PLAYERS
P1 = Player(
    canvas=screen,
    path=os.path.join("assets", "Character1.png"),
    keys=(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d),
    speed=5,
    x=center[0]-32,
    y=center[1],
    img_scale=2
)
P2 = Player(
    canvas=screen,
    path=os.path.join("assets", "Character2.png"),
    keys=(pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT),
    speed=5,
    x=center[0]+32,
    y=center[1],
    img_scale=2
)

# INTERACTION
pygame.key.set_repeat(10)


### EVENT LOOP ###
while True:
    screen.fill(black)
    pygame.event.pump()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
            keys = ['']*8
            for key in P1.keys+P2.keys:
                if pressed[key]:
                    keys.append(key)
            P1.move((P2,), keys)
            P2.move((P1,), keys)

    P1.render(screen)
    P2.render(screen)

    pygame.display.flip()
