### IMPORTS ###
import os
import random
import sys
import time

import pygame
from objects import Enemy, Flame, Pickup, Platform, Player, Object


### CONSTANTS ###
pygame.init()

# COLOURS
black = (0, 0, 0)
darkflame = (200, 92, 52)
flame = (235, 92, 52)
snow = (230, 240, 255)
white = (255, 255, 255)

# DISPLAY
screen = pygame.display.set_mode()
size = width, height = screen.get_size()
font = pygame.font.Font(r'assets\Grand9K Pixel.ttf', min(size)//16)
center = (width//2, height//2)
scale = speed = width//1000

# OBJECTS
Pl1 = Platform(
    canvas=screen,
    path=os.path.join("assets", "Platform.png"),
    x=center[0]+16*scale,
    y=0,
    img_scale=scale
)
Pl2 = Platform(
    canvas=screen,
    path=os.path.join("assets", "Platform.png"),
    x=center[0]+16*scale,
    y=height-32*scale,
    img_scale=scale
)
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
E1 = Enemy(
    canvas=screen,
    path=os.path.join("assets", "Crystal.png"),
    x=center[0]-16*scale,
    y=16+16*scale,
    img_scale=3,
    projectile=os.path.join("assets", "Ice_proj.png")
)
E2 = Enemy(
    canvas=screen,
    path=os.path.join("assets", "Crystal.png"),
    x=center[0]-16*scale,
    y=height-(32*scale),
    img_scale=3,
    projectile=os.path.join("assets", "Ice_proj.png")
)

# box = Object(canvas=screen, path=os.path.join("assets", "Stone1.png"), x=400, y=123, img_scale=10)

# INTERACTION
pygame.key.set_repeat(5*speed)
charge = 0
pickups = []
fcounter = 1
fguaranteed = 60*30


### Menus ###
def endgame(won=False):
    screen.fill(black)
    text = None
    if won == True:
        text = font.render("You won!", False, flame)
    elif won == False:
        text = font.render("You died!", False, flame)
    else:
        text = font.render("Game ended!", False, flame)
    textrect = text.get_rect()
    textrect.center = center
    screen.blit(text, textrect)
    pygame.display.flip()
    time.sleep(0.75)
    pygame.event.clear()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


### EVENT LOOP ###
while True:
    if playerflame.value <= 0:
        endgame()
        break

    screen.fill(snow)
    pygame.event.pump()
    if not random.randrange(0, 1000) or fcounter == fguaranteed:
        pickups.append(Pickup(screen, os.path.join("assets", "Stone1.png"), random.randrange(0, width), random.randrange(0, height), scale))
        fcounter = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            endgame('/')
            break
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            P1.rect.x, P1.rect.y = center[0]-32, center[1]
            P2.rect.x, P2.rect.y = center[0]+32, center[1]
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if charge > 700:
                    charge = 700
                if playerflame.value > 100:
                    P1.shoot(charge)
                    v = playerflame.value - 100
                    playerflame.value -= min(charge/2, v if v > 100 else 0)
                    charge = 0

    if mb := pygame.mouse.get_pressed():
        if mb[2]:
            charge = 0
        elif mb[0]:
            charge += 1

    if any(pressed := pygame.key.get_pressed()):
        keys = ['']*8
        for key in P1.keys+P2.keys:
            if pressed[key]:
                keys.append(key)
        P1.move((E1, P2), keys)
        P2.move((E1, P1), keys)


    ### DISPLAY UPDATES ###
    Pl1.render()
    Pl2.render()
    for pickup in pickups:
        pickup.render()
        if pickup.apply([P2]):
            pickups.remove(pickup)
    for shot in P1.shots:
        shot.render()
        shot.move((E1, *E1.shots))
    P1.render()
    P2.render()
    E1.update((P1, P2, *P1.shots))
    E2.update((P1, P2, *P1.shots))
    playerflame.value = round(playerflame - Flame(0.1), 1)
    pygame.draw.rect(screen, flame, (center[0]-playerflame.value/4, height-16, playerflame.value/2, 10), border_radius=5)
    if all([Pl1.press((P1, P2)), Pl2.press((P1, P2))]):
        endgame(True)
        break

    pygame.display.flip()
    pygame.time.Clock().tick(165)

pygame.quit()
sys.exit()
