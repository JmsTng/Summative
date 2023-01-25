import pygame

def start(screen, size, font, scale):
    splash = pygame.Surface(size)
    factor = 0
    word_frost = font.render("FROST", True, (149, 230, 237))
    word_frost_width, word_frost_height = word_frost.get_size()
    word_thaw = font.render("THAW", True, (235, 92, 52))
    word_thaw_width, word_thaw_height = word_thaw.get_size()
    while factor <= 1:
        splash.fill((0, 0, 0))
        tword_frost = pygame.transform.scale(word_frost, (int(word_frost_width*factor), int(word_frost_height*factor)))
        tword_thaw = pygame.transform.scale(word_thaw, (int(word_thaw_width*factor), int(word_thaw_height*factor)))
        word_width = tword_frost.get_width() + tword_thaw.get_width()
        splash.blit(tword_frost, (size[0]/2-word_width/2, size[1]/2-tword_frost.get_height()))
        splash.blit(tword_thaw, (size[0]/2-word_width/2+tword_frost.get_width(), size[1]/2-tword_thaw.get_height()))
        screen.blit(splash, (0, 0))
        pygame.display.flip()
        factor += 0.001
    alpha = 255
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                for _ in range(1000):
                    screen.fill((230, 240, 255))
                    splash.set_alpha(alpha)
                    screen.blit(splash, (0, 0))
                    pygame.display.flip()
                    alpha -= 255/1000
                return

# def intro(screen):