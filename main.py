### IMPORTS ###
import os
import sys

import pygame
from player import Player


### CONSTANTS ###
pygame.init()
pygame.key.set_repeat(10)

# COLOURS
black = (0, 0, 0)
white = (255, 255, 255)

# DISPLAY
screen = pygame.display.set_mode()
size = width, height = screen.get_size()
center = (width//2, height//2)

# PLAYERS
P1 = Player(os.path.join("assets", "character1.png"), ('w', 'a', 's', 'd'), y=center[1]-32)
P2 = Player(os.path.join("assets", "character2.png"), ('u', 'l', 'd', 'r'), y=center[1]+32)


### EVENT LOOP ###
while True:
    pygame.event.pump()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
            keys = ['']*4
            keys.append('w' if pressed[pygame.K_w] else '')
            keys.append('a' if pressed[pygame.K_a] else '')
            keys.append('s' if pressed[pygame.K_s] else '')
            keys.append('d' if pressed[pygame.K_d] else '')
            P1.move(screen, keys)
            keys = ['']*4
            keys.append('u' if pressed[pygame.K_UP] else '')
            keys.append('l' if pressed[pygame.K_LEFT] else '')
            keys.append('d' if pressed[pygame.K_DOWN] else '')
            keys.append('r' if pressed[pygame.K_RIGHT] else '')
            P2.move(screen, keys)
            
