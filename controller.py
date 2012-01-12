import pygame

import display

from pygame.locals import *

BUTTON_A, UP, DOWN, RIGHT, LEFT = range(5)

class Controller(object):

    def __init__(self):
        self.keymap = {BUTTON_A:False, LEFT:False, UP:False, RIGHT:False, DOWN:False}
        self._pos = None
        self.button_a = False

    def pos(self):
        x, y = self._pos if self._pos else pygame.mouse.get_pos()
        return (x, display.HEIGHT - y)

    def poll(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                return False
            if (e.type == KEYDOWN and e.key == K_ESCAPE):
                pygame.quit()
                return False
            if e.type == JOYAXISMOTION:
                x , y = j.get_axis(0), j.get_axis(1)
                self.keymap[RIGHT] = True if x > 0.7 else False
                self.keymap[UP] = True if y < -0.7 else False
                self.keymap[LEFT] = True if x < -0.7 else False
                self.keymap[DOWN] = True if y > 0.7 else False
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
            elif e.type == KEYDOWN:
                self._set_arrow_keymap(e, True)
            elif e.type == KEYUP:
                self._set_arrow_keymap(e, False)
        return True

    def _set_arrow_keymap(self, key, flag):
        if e.key == K_a:
            self.keymap[LEFT] = flag
        elif e.key == K_d:
            self.keymap[RIGHT] = flag
        elif e.key == K_w:
            self.keymap[UP] = flag
        elif e.key == K_s:
            self.keymap[DOWN] = flag
