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
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if not controller.poll():
            if hasattr(scene, 'server'):
                print 'shutdown'
                scene.server.shutdown()
            return
        scene.draw()
        pygame.display.flip()
        scene = scene.action(controller)

if __name__ == '__main__':
    main()
