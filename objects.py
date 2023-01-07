import pygame

class Object:
    '''Base class for all entities.'''
    def __init__(self, canvas:pygame.Surface, path:str, x:int=0, y:int=0, img_scale:float=1):
        img = pygame.image.load(path)
        self.canvas = canvas
        self.img = pygame.transform.scale(img, img_scale)
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def render(self, canvas=None):
        canvas = self.canvas if not canvas
        canvas.blit(self.img)
        
class Player(Object):
    def __init__(self, *, canvas:pygame.Surface, path:str, keys:tuple, x:int=0, y:int=0, img_scale:float=1):
        super().__init__(canvas, path, x, y, img_scale)
        self.keys = keys

    def move(self, keys):
        