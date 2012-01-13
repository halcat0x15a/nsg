from text import *

import socket

import server
from client import Client

import scene

IP_BOUNDS = (620,510,130,30)
TITLE_BOUNDS = (80,500,180,53)
NEXT_BOUNDS = (95,50,100,50)

class Lobby(object):

    def __init__(self):
        server.create_server()
        self.client = Client()
        self.title = Text("IP List", fontsize=160, color=BLACK)
        self.botton = Text("Next", fontsize=160, color=BLACK)
        self.ip_list = []

    def _index_bounds(self, i):
        x, y, width, height = IP_BOUNDS
        return (x, y - i * 50, width, height)

    def draw(self):
        self.title.draw(TITLE_BOUNDS)
        self.botton.draw(NEXT_BOUNDS)
        for i, ip in enumerate(self.ip_list):
            ip.draw(self._index_bounds(i))

    def action(self, controller):
        if controller.button_a and scene.contains(NEXT_BOUNDS, controller):
            return
        print self.client.send(None)
        return self

