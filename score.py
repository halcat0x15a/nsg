from text import *

from title import Title

RESULT_BOUNDS = (300, 200, 200, 50)

class Score(object):

    def __init__(self, win):
        self.result = Text("Win", fontsize=160, color=BLACK) if win else Text("Lose", fontsize=160, color=BLACK)

    def draw(self):
        self.result.draw(RESULT_BOUNDS)

    def action(self, controller):
        if controller.button_a:
            return Title()
        return self
