class Object(object):

    def draw(self):
        pass

class Player(Object):
    
    def __init__(self, coordinates=(0, 0, 0), eye=(0, 0, 0)):
        self.coordinates = coordinates
        self.eye = eye
        self.waiting = False
        self.life = 100
