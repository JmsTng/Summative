import pygame

class Object:
    '''Base class for all entities.'''
    def __init__(self, canvas:pygame.Surface, path:str=None, x:int=0, y:int=0, img_scale:float=1):
        img = pygame.image.load(path)
        w = img.get_width()
        h = img.get_height()
        self.img = pygame.transform.scale(img, (w*img_scale, h*img_scale))
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
        res = ([], [])
        for e in entities:
            r = e.rect
            if self.rect.clipline(r.right, r.top, r.right, r.bottom):
                res[0].append('l')
            if self.rect.clipline(r.left, r.top, r.left, r.bottom):
                res[0].append('r')
            if self.rect.clipline(r.left, r.bottom, r.right, r.bottom):
                res[0].append('u')
            if self.rect.clipline(r.left, r.top, r.right, r.top):
                res[0].append('d')
            res[1].append(e)
        
        return res
    
    def render(self, canvas=None, color=None, solid=False):
        canvas = self.canvas if not canvas else canvas
        if solid:
            pygame.draw.rect(canvas, color, self.rect)
        else:
            canvas.blit(self.img, self.rect)


class Pickup(Object):
    '''Class for objects that can be picked up.'''
    def __init__(self, canvas:pygame.Surface, path:str, x:int=0, y:int=0, img_scale:float=1):
        super().__init__(canvas=canvas, path=path, x=x, y=y, img_scale=img_scale)
    
    # def apply(self):
    #     collide = self.collides(P1, P2)
    #     if collide[1]:
    #         self.destroy()


# class Portal(Object):
#     '''For end puzzle/objective.'''
#     def __init__(self):


class Flame:
    '''Class to represent main game resource.'''
    def __init__(self, value:int=1000):
        self.value = value
    
    def __add__(self, other):
        if type(other) == type(Flame):
            return self.value + other.value
        elif type(other) == type(int):
            return self.value + other
    
    def __sub__(self, other):
        if type(other) == Flame:
            return self.value - other.value
        elif type(other) == int:
            return self.value - other
    


class Player(Object):
    '''Class to represent playble characters.'''
    def __init__(self, canvas:pygame.Surface, path:str, keys:tuple, *, speed:float, x:int=0, y:int=0, img_scale:float=1, flame:Flame):
        super().__init__(canvas=canvas, path=path, x=x, y=y, img_scale=img_scale)
        self.keys = keys
        self.speed = speed
        self.flame = flame

    def move(self, entities, keys):
        blocked = set(self.collides(entities)[0] + self.in_bounds(self.canvas.get_size()))
        vector = [0, 0]
        if self.keys[0] in keys and 'u' not in blocked:
            vector[1] -= self.speed
        if self.keys[1] in keys and 'l' not in blocked:
            vector[0] -= self.speed
        if self.keys[2] in keys and 'd' not in blocked:
            vector[1] += self.speed
        if self.keys[3] in keys and 'r' not in blocked:
            vector[0] += self.speed
            
        self.rect.move_ip(vector)
        
    def in_bounds(self, size):
        res = []
        if self.rect.y <= 0:
            res.append('u')
        if self.rect.x <= 0:
            res.append('l')
        if self.rect.y+self.rect.h >= size[1]:
            res.append('d')
        if self.rect.x+self.rect.w >= size[0]:
            res.append('r')
        
        return res
