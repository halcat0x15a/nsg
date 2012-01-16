import pygame

import display

from pygame.locals import *

BUTTON_A, UP, DOWN, RIGHT, LEFT = range(5)

class Controller(object):

    def __init__(self):
        self._pos = None
        self.button_a = False
        self.current_key = None
        self.left = False
        self.right = False
        self.up = False
        self.down = False

    def pos(self):
        x, y = self._pos if self._pos else pygame.mouse.get_pos()
        return (x, display.HEIGHT - y)

    def rel(self):
        return self._rel

    def poll(self):
        self._rel = (0, 0)
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                return False
            if (e.type == KEYDOWN and e.key == K_ESCAPE):
                pygame.quit()
                return False
            if e.type == JOYAXISMOTION:
                x , y = j.get_axis(0), j.get_axis(1)
                self.left = True if x < -0.7 else False
                self.right = True if x > 0.7 else False
                self.up = True if y < -0.7 else False
                self.down = True if y > 0.7 else False
            elif e.type == JOYHATMOTION:
                self._pos = (j.get_hat(0), j.get_hat(1))
            elif e.type == JOYBUTTONDOWN:
                pass
            elif e.type == JOYBUTTONUP:
                pass
            elif e.type == MOUSEBUTTONDOWN:
                self.button_a = True
            elif e.type == MOUSEBUTTONUP:
                self.button_a = False
            elif e.type == MOUSEMOTION:
                self._rel = e.rel
            elif e.type == KEYDOWN:
                key = e.key
                self.current_key = key
                self._set_arrow_keymap(key, True)
            elif e.type == KEYUP:
                self._set_arrow_keymap(e.key, False)
        return True

    def _set_arrow_keymap(self, key, flag):
        if key == K_a:
            self.left = flag
        elif key == K_d:
            self.right = flag
        elif key == K_w:
            self.up = flag
        elif key == K_s:
            self.down = flag
