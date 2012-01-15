from text import *

import socket

from server import *
from client import Client

import scene

from host_character_select import HostCharacterSelect

IP_BOUNDS = (620,510,130,30)
TITLE_BOUNDS = (80,500,180,53)
NEXT_BOUNDS = (95,50,100,50)

class Lobby(object):

    def __init__(self):
        identity = id(object())
        self.server = create_server(identity)
        self.client = Client(identity, host())
        self.title = Text("IP List", fontsize=160, color=BLACK)
        self.next = Text("Next", fontsize=160, color=BLACK)
        self.ip_list = []

    def _index_bounds(self, i):
        x, y, width, height = IP_BOUNDS
        return (x, y - i * 50, width, height)

    def draw(self):
        self.title.draw(TITLE_BOUNDS)
        self.next.draw(NEXT_BOUNDS)
        for i, ip in enumerate(self.ip_list):
            text = Text(str(ip), fontsize=80, color=BLACK)
            text.draw(self._index_bounds(i))
            del text

    def action(self, controller):
        if controller.button_a and scene.contains(NEXT_BOUNDS, controller.pos()):
            self.client.send(CHARACTER_SELECT)
            return HostCharacterSelect(self.server, self.client)
        self.ip_list = self.client.send(None) 
        return self

