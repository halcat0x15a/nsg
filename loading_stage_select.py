from text import *

from server import *

from battle import Battle

WAIT_BOUNDS = (290,280,220,35)

class LoadingStageSelect(object):

    def __init__(self, client):
        self.client = client
        self.wait = Text("Wait a minute", fontsize=80, color = BLACK)

    def draw(self):
        self.wait.draw(WAIT_BOUNDS)

    def action(self, controller):
        stage = self.client.send(None)
        return Battle(self.client)
