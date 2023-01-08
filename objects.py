import pygame

class Object:
    '''Base class for all entities.'''
    def __init__(self, canvas:pygame.Surface, path:str=None, color:str=None, x:int=0, y:int=0, w:int=0, h:int=0, img_scale:float=1):
        if path: # from path
            img = pygame.image.load(path)
            w = img.get_width()
            h = img.get_height()
            self.img = pygame.transform.scale(img, (w*img_scale, h*img_scale))
        else: # 
            self.color = color
        self.canvas = canvas
        self.rect = pygame.Rect(x, y, w*img_scale, h*img_scale)
        
    def near(self, entities):
        entities = list(entities)
        
        for e in entities:
            if self.rect.right not in range(e.rect.left-64, e.rect.left+160) or \
               self.rect.bottom not in range(e.rect.top-64, e.rect.top+160):
                entities.remove(e)
                continue
        
        return entities
    
    def collides(self, entities):
        entities = self.near(entities)
        free = ['l', 'r', 'u', 'd']
        for e in entities:
            e = e.rect
            if self.rect.clipline(e.right, e.top, e.right, e.bottom):
                free.remove('l')
            if self.rect.clipline(e.left, e.top, e.left, e.bottom):
                free.remove('r')
            if self.rect.clipline(e.left, e.bottom, e.right, e.bottom):
                free.remove('u')
            if self.rect.clipline(e.left, e.top, e.right, e.top):
                free.remove('d')
        
        return free
        
    def render(self, canvas=None, color=None, solid=False):
        canvas = self.canvas if not canvas else canvas
        if solid:
            pygame.draw.rect(canvas, color, self.rect)
        else:
            canvas.blit(self.img, self.rect)
        
class Player(Object):
    '''Class to represent playble characters.'''
    def __init__(self, *, canvas:pygame.Surface, path:str, keys:tuple, speed:float, x:int=0, y:int=0, img_scale:float=1):
        super().__init__(canvas=canvas, path=path, x=x, y=y, img_scale=img_scale)
        self.keys = keys
        self.speed = speed

    def move(self, entities, keys):
        free = self.collides(entities)
        vector = [0, 0]
        if self.keys[0] in keys and free.count('u'):
            vector[1] -= self.speed
        if self.keys[1] in keys and free.count('l'):
            vector[0] -= self.speed
        if self.keys[2] in keys and free.count('d'):
            vector[1] += self.speed
        if self.keys[3] in keys and free.count('r'):
            vector[0] += self.speed
            
        self.rect.move_ip(vector)
