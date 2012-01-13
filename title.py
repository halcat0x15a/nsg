from text import *

import scene

from login import Login
from lobby import Lobby

TITLE_BOUNDS = (200,400,400,70)
START_BOUNDS = (360,250,80,35)
HOST_BOUNDS = (232,250,70,35)
GUEST_BOUNDS = (489,250,90,35)
WAIT_BOUNDS = (290,280,220,35)

START_MENU, PLAYER_SELECT = range(2)

class Title(object):

    def __init__(self):
        self.mode = START_MENU
        self.title = Text("NSG WARS", fontsize=160, color=BLACK)
        self.start = Text("Start", fontsize=80, color=BLACK)
        self.host = Text("Host", fontsize=80, color=BLACK)
        self.guest = Text("Guest", fontsize=80, color=BLACK)
        self.wait = Text("Wait a minute", fontsize=80, color = BLACK)

    def _start_menu_draw(self):
        self.title.draw(TITLE_BOUNDS)
        self.start.draw(START_BOUNDS)

    def _player_select_draw(self):
        self.title.draw(TITLE_BOUNDS)
        self.host.draw(HOST_BOUNDS)
        self.guest.draw(GUEST_BOUNDS)

    def draw(self):
        {START_MENU:self._start_menu_draw, PLAYER_SELECT:self._player_select_draw}[self.mode]()

    def _start_menu_action(self, controller):
        if controller.button_a and scene.contains(START_BOUNDS, controller):
            self.mode = PLAYER_SELECT
        return self

    def _player_select_action(self, controller):
        if controller.button_a and scene.contains(HOST_BOUNDS, controller):
            return Lobby()
        elif controller.button_a and scene.contains(GUEST_BOUNDS, controller):
            return Login()
        return self

    def action(self, controller):
        return {START_MENU:self._start_menu_action, PLAYER_SELECT:self._player_select_action}[self.mode](controller)
