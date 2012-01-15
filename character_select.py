from image import Image
from text import *

import scene

from objects import PLAYERS

CHARACTERS_BOUNDS = [(120,300,150,150), \
                     (120,80,150,150), \
                     (320,300,150,150), \
                     (320,80,150,150), \
                     (520,300,150,150), \
                     (520,80,150,150)]
TITLE_BOUNDS = (80,500,180,53)

class CharacterSelect(object):

    def __init__(self, client):
        self.client = client
        self.player = None
        self.title = Text("Character select", fontsize=160, color=BLACK)
        self.characters = [Image('world1'), \
                           Image('world2'), \
                           Image('world3'), \
                           Image('world4'), \
                           Image('world5'), \
                           Image('world6')]

    def draw(self):
        self.title.draw(TITLE_BOUNDS)
        for i, image in enumerate(self.characters):
            if i == self.player:
                bounds = [x + 10 for x in CHARACTERS_BOUNDS[i]]
                image.draw(bounds)
            else:
                image.draw(CHARACTERS_BOUNDS[i])

    def action(self, controller):
        pos = controller.pos()
        for i, bounds in enumerate(CHARACTERS_BOUNDS):
             if controller.button_a and scene.contains(bounds, pos):
                 self.player = i
                 self.client.send(PLAYERS[i])

