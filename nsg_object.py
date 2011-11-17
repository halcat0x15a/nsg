from gameobjects import vector3

class NSGObject(object):

    def draw(self):
        pass

class Player(NSGObject):
    
    def __init__(self, coordinates=(0, 0, 0), eye=(0, 0, 0)):
        self.coordinates = coordinates
        self.eye = eye

