from pygame import image
class Player:
    def __init__(self, *, keys, x:int=0, y:int=0):
        img = image.load(img)
        self.rect = img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.keys = keys

    def move(self, *, keys):
        '''Move the player and handles collision with screen borders.'''
        vector = [0, 0]
        if not (i := self.keys[0] in keys and (j := self.keys[2] in keys)):
            vector[0] = 4 if i else -4 if j else 0
        if not (i := self.keys[1] in keys and (j := self.keys[3] in keys)):
            vector[1] = 4 if i else -4 if j else 0