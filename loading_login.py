from text import *

from server import *

from gest_character_select import GestCharacterSelect

WAIT_BOUNDS = (290,280,220,35)

class LoadingLogin(object):

    def __init__(self, client):
        self.client = client
        self.wait = Text("Wait a minute", fontsize=80, color = BLACK)

    def draw(self):
        self.wait.draw(WAIT_BOUNDS)

    def action(self, controller):
        mode = self.client.send(None)
        if mode == LOGIN:
            return self
        elif CHARACTER_SELECT:
            return GestCharacterSelect(self.client)
