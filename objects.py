import pygame
class Object:
    '''Base class for any entity.'''
    def __init__(self, canvas, img:str, x:int, y:int):
        self.canvas = canvas
        self.img = pygame.image.load(img)
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def collides(self, players):
        '''Check for collision with players.'''
        print(self.rect.collidelistall(players))
    
    def render(self, canvas=None):
        '''Draw object to screen.'''
        if canvas == None:
            canvas = self.canvas
        canvas.blit(self.img, self.rect)

class Nonsolid(Object):
    '''Base class for nonsolid entities.'''
    

class Solid(Object):
    '''Base class for solid entities.'''
    def __init__(self, canvas, img:str, x:int, y:int):
        super().__init__(canvas, img, x, y)

class Player(Object):
    '''General class for playable character.'''
    def __init__(self, canvas, img:str, keys:tuple, speed:int=5, x:int=0, y:int=0):
        super().__init__(canvas, img, x, y)
        self.keys = keys
        self.speed = speed

    def move(self, keys):
        '''Moves the player.'''
        vector = [0, 0]
        checks = self.in_bounds(self.canvas.get_size())
        if self.keys[0] in keys:
            if checks[1] != self.speed+1:
                vector[1] -= self.speed if checks[1] == True else checks[1]
        if self.keys[2] in keys:
            if checks[1] != self.speed+2:
                vector[1] += self.speed if checks[1] == True else checks[1]
        if self.keys[1] in keys:
            if checks[0] != self.speed+1:
                vector[0] -= self.speed if checks[0] == True else checks[0]
        if self.keys[3] in keys:
            if checks[0] != self.speed+2:
                vector[0] += self.speed if checks[0] == True else checks[0]
                
        self.rect.move_ip(vector)

    def in_bounds(self, size):
        '''Checks whether the player is within the playing area.'''
        checks = [True, True]
        
        # Horizontal
        if self.rect.left-self.speed < 0:
            if self.rect.left <= 0: checks[0] = self.speed+1
            else: checks[0] = self.rect.left - self.speed
        elif self.rect.right+self.speed > size[0]:
            if self.rect.right >= size[0]: checks[0] = self.speed+2
            else: checks[0] = self.rect.right + self.speed - size[0]
        
        # Vertical
        if self.rect.top-self.speed < 0:
            if self.rect.top <= 0: checks[1] = self.speed+1
            else: checks[1] = self.rect.top - self.speed
        elif self.rect.bottom+self.speed > size[1]:
            if self.rect.bottom >= size[1]: checks[1] = self.speed+2
            else: checks[1] = self.rect.bottom + self.speed - size[1]
            
        return checks
