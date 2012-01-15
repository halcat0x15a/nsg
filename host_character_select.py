from image import Image
from text import *

import scene

from server import *

from character_select import CharacterSelect

from stage_select import StageSelect

from objects import PLAYERS

NEXT_BOUNDS = (95,50,100,50)

class HostCharacterSelect(object):

    def __init__(self, server, client):
        self.server = server
        self.client = client
        self.next = Text("Next", fontsize=160, color=BLACK)
        self.scene = CharacterSelect(client)

    def draw(self):
        self.next.draw(NEXT_BOUNDS)
        self.scene.draw()

    def action(self, controller):
        self.scene.action(controller)
        pos = controller.pos()
        if controller.button_a and scene.contains(NEXT_BOUNDS, pos):
            self.client.send(STAGE_SELECT)
            return StageSelect(self.server, self.client)
        return self
