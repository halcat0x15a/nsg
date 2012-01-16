from image import Image
from text import *

import scene

from battle import Battle

WORLDS_BOUNDS = [(120,300,150,150), \
                     (120,80,150,150)]
TITLE_BOUNDS = (80,500,220,53)

class StageSelect(object):

    def __init__(self, server, client, player_id):
        self.server = server
        self.client = client
        self.player_id = player_id
        self.title = Text("Stage Select", fontsize=160, color=BLACK)
        self.worlds = [Image('world1'), \
                       Image('world2')]

    def draw(self):
        self.title.draw(TITLE_BOUNDS)
        for i, world in enumerate(self.worlds):
            world.draw(WORLDS_BOUNDS[i])

    def action(self, controller):
        pos = controller.pos()
        for i, bounds in enumerate(WORLDS_BOUNDS):
            if controller.button_a and scene.contains(bounds, pos):
                self.client.send(i)
                s = Battle(self.client, self.player_id, i)
                s.server = self.server
                return s
        return self
