class Object(object):

    def draw(self):
        pass

    def __eq__(self, other):
        return hasattr(other, '__dict__') and self.__dict__ == other.__dict__

class Player(Object):
    
    def __init__(self, coordinates=(0, 0, 0), eye=(0, 0, 0)):
        self.coordinates = coordinates
        self.eye = eye
        self.waiting = False
        self.life = 100

IT = Player()

EM = Player()

ID = Player()

DD = Player()

IB = Player()

FC = Player()

PLAYERS = [IT, EM, ID, DD, IB, FC]
