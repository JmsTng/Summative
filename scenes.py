import pygame


def center_axis(a, b):
    return a/2-b/2


def center(surface, size, x_offset=0, y_offset=0, force=(False, False)):
    return \
        center_axis(size[0], 0 if force[0] else surface.get_width())+x_offset,\
        center_axis(size[1], 0 if force[1] else surface.get_height())+y_offset


def render_text(text, font, color, size, canvas, *, scale=1, x_offset=0, y_offset=0, force=(False, False)):
    text = font.render(text, False, color)
    text = pygame.transform.scale(text, (int(text.get_width()*scale), int(text.get_height()*scale)))
    canvas.blit(text, center(text, size, x_offset, y_offset, force))
    pygame.display.flip()


def start(screen, size, title_font, body_font):
    splash = pygame.Surface(size)
    wf = title_font.render("FROST", False, (149, 230, 237))
    wt = title_font.render("THAW", False, (235, 92, 52))
    wfw, wh = wf.get_size()
    wtw, wh = wt.get_size()
    ww = wfw + wtw
    factor = 0
    while factor <= 1:
        splash.fill((0, 0, 0))
        tword_frost = pygame.transform.scale(wf, (int(wfw * factor), int(wh * factor)))
        tword_thaw = pygame.transform.scale(wt, (int(wtw * factor), int(wh * factor)))
        tww = ww * factor
        splash.blit(tword_frost, (size[0]/2-tww/2, size[1]/2-wh*factor-64))
        splash.blit(tword_thaw, (size[0]/2-tww/2+tword_frost.get_width(), size[1]/2-wh*factor-64))
        screen.blit(splash, (0, 0))
        pygame.display.flip()
        factor += 0.005
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                factor = 1
                pygame.event.clear()
                break

    # things to draw and math
    tip = body_font.render("Press any key to continue", False, (255, 255, 255))
    text_play = body_font.render("Play", False, (0, 0, 0))
    tpw, tph = text_play.get_size()
    tpx, tpy = center(text_play, size)
    btn_play = pygame.Rect(tpx-32, tpy-6, tpw+64, tph+16)
    text_rules = body_font.render("Rules", False, (0, 0, 0))
    tgw, tgh = text_play.get_size()
    tgx, tgy = center(text_play, size)
    btn_rules = pygame.Rect(tpx-32, tpy-6, tpw+64, tph+16)

    # drawing
    splash.blit(tip, (size[0]/2-tip.get_width()/2, size[1]/2-64))
    pygame.draw.rect(splash, (255, 255, 255), btn_play, border_radius=2)
    splash.blit(text_play, center(text_play, size))
    screen.blit(splash, (0, 0))
    pygame.display.flip()
    alpha = 255
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                for _ in range(500):
                    screen.fill((230, 240, 255))
                    splash.set_alpha(alpha)
                    screen.blit(splash, (0, 0))
                    pygame.display.flip()
                    alpha -= 255/500
                pygame.event.clear()
                return

# def intro(screen):


def end(screen, title_font, won=False):
    import sys, time
    screen.fill((0, 0, 0))
    text = None
    if won is True:
        text = title_font.render("You won!", False, (235, 92, 52))
    elif won is False:
        text = title_font.render("You died!", False, (235, 92, 52))
    else:
        text = title_font.render("Game ended!", False, (235, 92, 52))
    textrect = text.get_rect()
    textrect.center = center(text, screen.get_size(), force=(True, True))
    screen.blit(text, textrect)
    pygame.display.flip()
    pygame.event.clear()
    time.sleep(0.75)
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
