from text import *

import socket

from server import *
from client import Client

from loading_login import LoadingLogin

from pygame.locals import *

IP_BOUNDS = (380,280,30,30)

class Login(object):

    def __init__(self):
        self.ip = '127.0.1.1'

    def _length_bounds(self, i):
        x, y, width, height = IP_BOUNDS
        return (x - (i - 1) * IP_BOUNDS[2] / 2, y, width + (i - 1) * IP_BOUNDS[2], height)

    def draw(self):
        ip = Text(self.ip, fontsize=80, color=BLACK)
        ip.draw(self._length_bounds(len(self.ip)))
        del ip

    def action(self, controller):
        key = controller.current_key
        if key == K_BACKSPACE:
            if self.ip:
                self.ip = self.ip[:-1]
        elif key == K_RETURN:
            try:
                client = Client(id(object()), self.ip)
                client.send(None)
                return LoadingLogin(client)
            except:
                self.ip = ''
        elif key:
            try:
                self.ip += chr(key)
            except:
                pass
        controller.current_key = None
        return self
