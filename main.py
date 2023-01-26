### IMPORTS ###
import os
import sys

import pygame
from objects import Enemy, Flame, Pickup, Platform, Player
from random import randrange
from scenes import start, end


### CONSTANTS ###
pygame.init()

# COLOURS
black = (0, 0, 0)
flame = (235, 92, 52)
snow = (230, 240, 255)
white = (255, 255, 255)

# DISPLAY
screen = pygame.display.set_mode()
pygame.display.set_caption("FROSTTHAW")
size = width, height = screen.get_size()
title_font = pygame.font.Font(os.path.join("assets", "font", "Grand9k Pixel.ttf"), min(size) // 16)
header_font = pygame.font.Font(os.path.join("assets", "font", "Grand9k Pixel.ttf"), min(size) // 32)
body_font = pygame.font.Font(os.path.join("assets", "font", "Grand9k Pixel.ttf"), min(size) // 64)
center = (width//2, height//2)
scale = speed = max(width//1000, 1)

# OBJECTS
playerflame = Flame()
Pl1 = Platform(canvas=screen, path=os.path.join("assets", "img", "Platform.png"), x=center[0], y=32*scale/2+16, img_scale=scale)
Pl2 = Platform(canvas=screen, path=os.path.join("assets", "img", "Platform.png"), x=center[0], y=height-32*scale/2-16, img_scale=scale)
P1 = Player(canvas=screen, path=os.path.join("assets", "img", "Character1.png"), keys=(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d), speed=speed, x=center[0]-32*scale, y=center[1], img_scale=scale, flame=playerflame)
P2 = Player(canvas=screen, path=os.path.join("assets", "img", "Character2.png"), keys=(pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT), speed=speed, x=center[0]+32*scale, y=center[1], img_scale=scale, flame=playerflame)

enemies = [
    Enemy(canvas=screen, path=os.path.join("assets", "img", "Crystal.png"), x=center[0], y=32*scale/2+40*scale, img_scale=3, projectile=os.path.join("assets", "img", "Ice_proj.png")),
    Enemy(canvas=screen, path=os.path.join("assets", "img", "Crystal.png"), x=center[0], y=height-32*scale/2-40*scale, img_scale=3, projectile=os.path.join("assets", "img", "Ice_proj.png"))
]

# INTERACTION
pygame.key.set_repeat(5*speed)
charge = 0
pickups = []
fcounter = 1
fguaranteed = 60*30


### Menus ###
pebbles = [
    (pygame.transform.scale(pygame.image.load(os.path.join("assets", "img", "Stone1.png")), (16, 16)),
     randrange(0, width),
     randrange(0, height)) for _ in range(20)
]
start(screen, size, title_font, body_font)


### EVENT LOOP ###
while True:
    if playerflame.value <= 0:
        end(screen, title_font)
        break

    screen.fill(snow)
    for p in pebbles:
        screen.blit(p[0], (p[1], p[2]))
    pygame.event.pump()
    if not randrange(0, 1000) or fcounter == fguaranteed:
        pickups.append(Pickup(screen, os.path.join("assets", "img", "Fire_Pickup.png"), randrange(0, width), randrange(0, height), scale))
        fcounter = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            end(screen, title_font, '/')
            break
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
        P1.move((*enemies, P2), keys)
        P2.move((*enemies, P1), keys)


    ### DISPLAY UPDATES ###
    Pl1.render()
    Pl2.render()
    for pickup in pickups:
        pickup.render()
        if pickup.apply(P2):
            pickups.remove(pickup)
    for shot in P1.shots:
        shot.render()
        shot.move([e for e in enemies])
    P1.render()
    P2.render()
    [e.update((P1, P2, *P1.shots)) for e in enemies]
    playerflame.value = round(playerflame - Flame(0.1), 1)
    pygame.draw.rect(screen, flame, (center[0]-playerflame.value/4, height-16, playerflame.value/2, 10), border_radius=5)
    if all([Pl1.press((P1, P2)), Pl2.press((P1, P2))]): end(screen, title_font, True)

    pygame.display.flip()
    pygame.time.Clock().tick(165)

pygame.quit()
sys.exit()
