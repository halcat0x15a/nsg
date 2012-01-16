import pygame

from OpenGL.GL import *
from OpenGL.GLU import *

SIZE = (800, 600)

WIDTH, HEIGHT = SIZE

def init():
    pygame.display.set_mode(SIZE, pygame.OPENGL|pygame.DOUBLEBUF)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, 0, HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
