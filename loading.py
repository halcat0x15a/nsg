from text import *

WAIT_BOUNDS = (290,280,220,35)

class Loading(object):

    def __init__(self):
        self.wait = Text("Wait a minute", fontsize=80, color = BLACK)

    def draw(self):
        self.wait.draw(WAIT_BOUNDS)

    def action(self, controller):
        return self
