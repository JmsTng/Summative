### IMPORTS ###
import os
import sys

import pygame
from objects import Flame, Player, Object


### CONSTANTS ###
pygame.init()

# COLOURS
black = (0, 0, 0)
snow = (230, 240, 255)
white = (255, 255, 255)

# DISPLAY
screen = pygame.display.set_mode()
size = width, height = screen.get_size()
center = (width//2, height//2)
scale = speed = width//1000

# OBJECTS
playerflame = Flame()
P1 = Player(
    canvas=screen,
    path=os.path.join("assets", "Character1.png"),
    keys=(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d),
    speed=speed,
    x=center[0]-32,
    y=center[1],
    img_scale=scale,
    flame=playerflame
)
P2 = Player(
    canvas=screen,
    path=os.path.join("assets", "Character2.png"),
    keys=(pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT),
    speed=speed,
    x=center[0]+32,
    y=center[1],
    img_scale=scale,
    flame=playerflame
)

box = Object(canvas=screen, path=os.path.join("assets", "Stone1.png"), x=400, y=123, img_scale=10)

# INTERACTION
pygame.key.set_repeat(5*speed)


### Menus ###


### EVENT LOOP ###
while True:
    if playerflame.value <= 0:
        print("you died")
        break

    screen.fill(snow)
    pygame.event.pump()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print("quit")
            break
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_r:
                    P1.rect.x, P1.rect.y = center[0]-32, center[1]
                    P2.rect.x, P2.rect.y = center[0]+32, center[1]
                case pygame.K_e:
                    playerflame.value = 1000 #testing
        
    if any(pressed := pygame.key.get_pressed()):
        keys = ['']*8
        for key in P1.keys+P2.keys:
            if pressed[key]:
                keys.append(key)
        P1.move((P2, box), keys)
        P2.move((P1, box), keys)

    P1.render(screen)
    P2.render(screen)
    playerflame.value = round(playerflame.value - 0.1, 1)
    pygame.draw.rect(screen, (235, 92, 52), (center[0]-playerflame.value/4, height-16, playerflame.value/2, 10), border_radius=5)
    box.render()

    pygame.display.flip()

pygame.quit()
sys.exit()
