from text import *

from server import *

from battle import Battle

WAIT_BOUNDS = (290,280,220,35)

class LoadingStageSelect(object):

    def __init__(self, client, player_id):
        self.client = client
        self.player_id = player_id
        self.wait = Text("Wait a minute", fontsize=80, color = BLACK)

    def draw(self):
        self.wait.draw(WAIT_BOUNDS)

    def action(self, controller):
        stage_id = self.client.send(None)
        return Battle(self.client, self.player_id, stage_id)
