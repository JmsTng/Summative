import pygame
from math import atan2, cos, degrees, radians, pi, sin, sqrt

def pythagoras(a, b):
    return sqrt(a*a + b*b)

class Object:
    '''Base class for all entities.'''
    def __init__(self, canvas:pygame.Surface, path:str, x:int=0, y:int=0, img_scale:float=1):
        img = pygame.image.load(path)
        w = img.get_width()
        h = img.get_height()
        self.img = pygame.transform.scale(img, (w*img_scale, h*img_scale))
        self.canvas = canvas
        self.rect = pygame.Rect(x, y, w*img_scale, h*img_scale)
        
    def near(self, entities):
        entities = list(entities)
        
        for e in entities:
            if not (e.rect.centerx-128 <= self.rect.centerx <= e.rect.centerx+128) or \
               not (e.rect.centery-128 <= self.rect.centery <= e.rect.centery+128):
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
        self.shots = []

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
    
    def shoot(self, charge, entities):
        self.shots.append(Projectile(self.canvas, r'assets\Fire_proj.png', 10, self, x=self.rect.centerx, y=self.rect.centery, img_scale=3))


class Enemy(Object):
    '''Crystal turret class'''
    def __init__(self, canvas:pygame.Surface, path:str, *, x:int=0, y:int=0, img_scale:float=1, projectile:str):
        super().__init__(canvas, path, x, y, img_scale)
        self.projectile = projectile
        self.shottimer = 0
        self.shots = []
        
    def shoot(self, entities):
        if self.shottimer == 100:
            self.shots.extend([
                Projectile(self.canvas, r'assets\Ice_proj.png', 5, self, angle=0, x=self.rect.centerx, y=self.rect.bottom, img_scale=3), # bottom
                Projectile(self.canvas, r'assets\Ice_proj.png', 5, self, angle=90, x=self.rect.right, y=self.rect.centery, img_scale=3), # right
                Projectile(self.canvas, r'assets\Ice_proj.png', 5, self, angle=180, x=self.rect.centerx, y=self.rect.top, img_scale=3), # top
                Projectile(self.canvas, r'assets\Ice_proj.png', 5, self, angle=270, x=self.rect.left, y=self.rect.centery, img_scale=3)]) # left
        elif self.shottimer == 200:
            self.shots.extend([
                Projectile(self.canvas, r'assets\Ice_proj.png', 5, self, angle=45, x=self.rect.centerx, y=self.rect.centery, img_scale=3),
                Projectile(self.canvas, r'assets\Ice_proj.png', 5, self, angle=135, x=self.rect.centerx, y=self.rect.centery, img_scale=3),
                Projectile(self.canvas, r'assets\Ice_proj.png', 5, self, angle=225, x=self.rect.centerx, y=self.rect.centery, img_scale=3),
                Projectile(self.canvas, r'assets\Ice_proj.png', 5, self, angle=315, x=self.rect.centerx, y=self.rect.centery, img_scale=3)])
            self.shottimer = 0
        else:
            for shot in self.shots:
                shot.move(entities)
                shot.render()
        self.shottimer += 1


class Projectile(Object):
    '''Generic class for projectiles.'''
    def __init__(self, canvas:pygame.Surface, path:str, speed:float, parent:Object, *, angle:int=None, x:int=0, y:int=0, img_scale:float=1, max_dist:int=450):
        super().__init__(canvas, path, x, y, img_scale)
        self.speed = speed
        self.parent = parent
        self.max_dist = max_dist
        if angle == None:
            mx, my = pygame.mouse.get_pos()
            angle = atan2(my-self.parent.rect.centery, mx-self.parent.rect.centerx)
            angle = degrees(angle)
        self.angle = angle
        self.img = pygame.transform.rotate(self.img, angle+90)
        
    def move(self, entities):
        blocked = set(self.collides(entities)[0] + self.in_bounds(self.canvas.get_size()))
        if pythagoras(abs(self.rect.centerx-self.parent.rect.centerx), abs(self.rect.centery-self.parent.rect.centery)) > self.max_dist or \
           blocked:
           return self.parent.shots.remove(self)
        
        self.rect.move_ip(self.speed*sin(radians(self.angle)), self.speed*cos(radians(self.angle)))
