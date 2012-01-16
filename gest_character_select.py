from image import Image

from server import *

import scene

from character_select import CharacterSelect

from loading_stage_select import LoadingStageSelect

from objects import PLAYERS

class GestCharacterSelect(object):

    def __init__(self, client):
        self.client = client
        self.scene = CharacterSelect(client)

    def draw(self):
        self.scene.draw()

    def action(self, controller):
        self.scene.action(controller)
        mode = self.client.send(None)
        if STAGE_SELECT == mode:
            return LoadingStageSelect(self.client, self.scene.player_id)
        return self
