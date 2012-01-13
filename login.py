from text import *

import socket

import server
from client import Client

import scene

from pygame.locals import *

IP_BOUNDS = (620,510,130,30)
TITLE_BOUNDS = (80,500,180,53)
NEXT_BOUNDS = (95,50,100,50)

class Login(object):

    def __init__(self):
        self.ip = ''

    def draw(self):
        ip = Text(self.ip, fontsize=160, color=BLACK)
        ip.draw()
        del ip

    def action(self, controller):
        key = controller.current_key
        if key == K_BACKSPACE:
            if self.ip:
                self.ip = self.ip[:-1]
        elif key:
            self.ip += chr(key)
            print self.ip
        controller.current_key = None
        return self

            
