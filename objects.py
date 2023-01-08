import pygame

class Object:
    '''Base class for all entities.'''
    def __init__(self, canvas:pygame.Surface, path:str, x:int=0, y:int=0, img_scale:float=1):
        img = pygame.image.load(path)
        w = img.get_width()
        h = img.get_height()
        self.canvas = canvas
        self.img = pygame.transform.scale(img, (w*img_scale, h*img_scale))
        self.rect = pygame.Rect(x, y, w, h)
        
    def near(self, entities):
        entities = list(entities)
        
        for e in entities:
            if self.rect.right not in range(e.rect.left-64, e.rect.left+128) \
               or self.rect.bottom not in range(e.rect.top-64, e.rect.top+128):
                entities.remove(e)
                continue
        
        return entities
    
    def collides(self, entities):
        entities = self.near(entities)
        free = ['l', 'r', 'u', 'd']
        for e in entities:
            e = e.rect
            if self.rect.clipline(e.x+e.w, e.y, e.x+e.w, e.y+e.h):
                free.remove('l')
            if self.rect.clipline(e.x, e.y, e.x, e.y+e.h):
                free.remove('r')
            if self.rect.clipline(e.x, e.y+e.h, e.x+e.w, e.y+e.h):
                free.remove('u')
            if self.rect.clipline(e.x, e.y, e.x+e.w, e.y):
                free.remove('d')
        
        return free
        
    def render(self, canvas=None):
        canvas = self.canvas if not canvas else canvas
        canvas.blit(self.img, self.rect)
        
class Player(Object):
    def __init__(self, *, canvas:pygame.Surface, path:str, keys:tuple, speed:float, x:int=0, y:int=0, img_scale:float=1):
        super().__init__(canvas, path, x, y, img_scale)
        self.keys = keys
        self.speed = speed

    def move(self, entities, keys):
        free = self.collides(entities)
        vector = (0, 0)
        if self.keys[0] in keys and free.index('u'):
            vector[1] -= 5
        if self.keys[1] in keys and free.index('l'):
            vector[0] -= 5
        if self.keys[2] in keys and free.index('d'):
            vector[1] += 5
        if self.keys[3] in keys and free.index('r'):
            vector[0] += 5
            
        self.rect.move_ip(vector)
