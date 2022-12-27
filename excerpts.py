def progress_loading_thing():
	# import sys
	# import time
	
	# import pygame
	
	
	# black = (0, 0, 0)
	# white = (255, 255, 255)
	
	
	# pygame.init()
	# font = pygame.font.Font("assets/pixel_font.ttf", 24)
	
	# size = width, height = 480, 720
	# screen = pygame.display.set_mode()
	
	
	# text = font.render("Idle", False, white)
	# rect = text.get_rect()
	# rect.center = (width/2, height/2)
	# progress = 0
	
	# pygame.key.set_repeat(50)
	
	# while True:
	# 	pygame.event.pump()
	# 	for event in pygame.event.get():
	# 		if event.type == pygame.QUIT:
	# 			sys.exit()
	# 		if event.type == pygame.KEYDOWN:
	# 			print(event.key)
	# 			if event.key == pygame.K_e:
	# 				if progress >= 100:
	# 					text = font.render("Complete.", False, white)
	# 				else:
	# 					progress += .1
	# 					text = font.render("Loading" + "."*(round(progress)%3+1), False, white)
	# 				bar = pygame.Rect(20, 20, progress, 30)
	# 				pygame.draw.rect(screen, white, bar)
	# 		elif event.type == pygame.KEYUP:
	# 			if event.key == pygame.K_e:
	# 				progress = 0
	# 				text = font.render("Idle", False, white)
	
	# 	screen.fill(black)
	# 	screen.blit(text, rect)
	# 	pygame.display.flip()