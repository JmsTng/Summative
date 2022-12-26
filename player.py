from pygame import image
class Player:
    def __init__(self, *, keys, x:int=0, y:int=0):
        img = image.load(img)
        self.rect = img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.keys = keys

    def move(self, canvas, *, keys):
        '''Move the player and handles collision with screen borders.'''
        vector = [0, 0]
        if not (i := self.keys[0] in keys and (j := self.keys[2] in keys)): # check for collision
            vector[0] = 5 if i else -5 if j else 0
        if not (i := self.keys[1] in keys and (j := self.keys[3] in keys)): # check for collision
            vector[1] = 5 if i else -5 if j else 0

        self.rect.move_ip(vector)