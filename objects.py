from math import *

class Object(object):

    def __eq__(self, other):
        return hasattr(other, '__dict__') and self.__dict__ == other.__dict__

    def _rad(self, r):
        return r * pi / 180

    def radx(self):
        return self._rad(self.rx)

    def rady(self):
        return self._rad(self.ry)

    def forward(self):
        self.x += self.v() * cos(self.radx())
        self.y += self.v() * sin(self.radx())

class Bullet(Object):

    def __init__(self, player):
        self.x = player.x
        self.y = player.y
        self.z = player.z
        self.rx = player.rx
        self.ry = player.ry
        self.dead = False

    def v(self):
        return 3

    def center_x(self):
        return self.x

    def center_y(self):
        return self.y

    def center_z(self):
        return self.z + 4

class Character(Object):
    
    def __init__(self, obj_id):
        self.waiting = False
        self.life = 100
        self.obj_id = obj_id
        self.rx = 0.
        self.ry = 0.
        self.x = 0.
        self.y = 0.
        self.z = 0.
        self.reaction = 0
        self.bullets = []

    def reset_reaction(self):
        self.reaction = 50

    def v(self):
        return 0.5

    def r(self):
        return 100

    def eye_x(self):
        return self.x

    def eye_y(self):
        return self.y

    def eye_z(self):
        return self.z + 7

    def center_x(self):
        return self.x + (self.r() * cos(self.radx()))

    def center_y(self):
        return self.y + (self.r() * sin(self.radx()))

    def center_z(self):
        return self.z + (self.r() * cos(self.rady()))

IT = Character(0)

EM = Character(1)

ID = Character(2)

DD = Character(3)

IB = Character(4)

FC = Character(5)

PLAYERS = [IT, EM, ID, DD, IB, FC]
