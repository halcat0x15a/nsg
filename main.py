import pygame
from OpenGL.GL import *
import display
from title import Title
from controller import Controller

def main():
    pygame.init()
    display.init()
    controller = Controller()
    scene = Title()
    while True:
        glClear(GL_COLOR_BUFFER_BIT)
        if not controller.poll():
            return
        new_scene = scene.action(controller)
        scene.draw()
        pygame.display.flip()
        scene = new_scene

if __name__ == '__main__':
    main()
