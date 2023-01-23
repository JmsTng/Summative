### IMPORTS ###
import os
import sys
import time

import pygame
from objects import Enemy, Flame, Player, Object


### CONSTANTS ###
pygame.init()

# COLOURS
black = (0, 0, 0)
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
    x=100,
    y=100,
    img_scale=3,
    projectile=os.path.join("assets", "Ice_proj.png")
)

box = Object(canvas=screen, path=os.path.join("assets", "Stone1.png"), x=400, y=123, img_scale=10)

# INTERACTION
pygame.key.set_repeat(5*speed)


### Menus ###
def endgame(won=False):
    screen.fill(black)
    text = None
    if won is True:
        text = font.render("You won!", False, flame)
    elif won is False:
        text = font.render("You died!", False, flame)
    else:
        text = font.render("Game ended!", False, flame)
    textrect = text.get_rect()
    textrect.center = center
    screen.blit(text, textrect)
    pygame.display.flip()
    time.sleep(1)
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

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            endgame('/')
            break
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_r:
                    P1.rect.x, P1.rect.y = center[0]-32, center[1]
                    P2.rect.x, P2.rect.y = center[0]+32, center[1]
                case pygame.K_e:
                    playerflame.value = 1000  # testing
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                P1.shoot(5, (P2, E1))
            elif event.button == 3:
                P2.shoot(5, (P1, E1))
        
    if any(pressed := pygame.key.get_pressed()):
        keys = ['']*8
        for key in P1.keys+P2.keys:
            if pressed[key]:
                keys.append(key)
        P1.move((P2, box), keys)
        P2.move((P1, box), keys)

    
    ### DISPLAY UPDATES ###
    P1.render()
    P2.render()
    for shot in P1.shots:
        shot.move((P2, E1))
        shot.render()
    E1.shoot((P1, P2))
    E1.render()
    playerflame.value = round(playerflame - Flame(0.1), 1)
    pygame.draw.rect(screen, flame, (center[0]-playerflame.value/4, height-16, playerflame.value/2, 10), border_radius=5)
    box.render()

    pygame.display.flip()
    time.sleep(0.01)

pygame.quit()
sys.exit()
