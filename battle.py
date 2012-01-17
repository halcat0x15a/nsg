import pygame
import display

import objects

from text import *

from OpenGL.GL import *
from OpenGL.GLU import *

from objloader import *

HP_BOUNDS = (650, 500, 100, 50)

class Battle(object):

    def _perspective(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90.0, display.WIDTH / float(display.HEIGHT), 1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def _ortho(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, display.WIDTH, 0, display.HEIGHT)
        glMatrixMode(GL_MODELVIEW)
    
    def __init__(self, client, player_id, stage_id):
        self.client = client
        glClearColor(0.0, 0.0, 1.0, 1.0)
        self._perspective()
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        glShadeModel(GL_SMOOTH)
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        field = OBJ('feildmap.obj', swapyz=True)
        fields = [field]
        it_obj = OBJ('ITchar.obj', swapyz=True)
        objs = [it_obj]
        self.obj = objs[0]
        self.field = fields[0]
        self.bullet_obj = OBJ('rifle1.obj', swapyz=True)#OBJ('ITkey.obj', swapyz=True)
        self.objects = self.client.send(objects.PLAYERS[player_id])

    def _range(self, obj, char):
        v_list = [[], [], []]
        for vertex in obj.vertices:
            for i, v in enumerate(vertex):
                v_list[i].append(v)
        v_range = []
        xyz = [char.x, char.y, char.z]
        for i, l in enumerate(v_list):
            l.sort()
            v_range.append((min(l) + xyz[i], max(l) + xyz[i]))
        return v_range

    def _contains(self, obj, s_char, t_char):
        xr, yr, zr = self._range(obj, s_char)
        def f(r, n):
            return n > r[0] and n < r[1]
        return f(xr, t_char.x) and f(yr, t_char.y) and f(zr, t_char.z)

    def draw(self):
        self._perspective()
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)
        player = self.objects[self.client.identity]
        glLoadIdentity()
        gluLookAt(player.eye_x(), player.eye_y(), player.eye_z(), player.center_x(), player.center_y(), player.center_z(), 0, 0, 1)
        glPushMatrix()
        glCallList(self.field.gl_list)
        glPopMatrix()
        for player in self.objects.values():
            glPushMatrix()
            glTranslate(player.x, player.y, player.z)
            glCallList(self.obj.gl_list)
            glPopMatrix()
            for bullet in player.bullets:
                glPushMatrix()
                glTranslate(bullet.center_x(), bullet.center_y(), bullet.center_z())
                glCallList(self.bullet_obj.gl_list)
                glPopMatrix()
        self._ortho()
        glDisable(GL_COLOR_MATERIAL)
        glDisable(GL_LIGHTING)
        glPushMatrix()
        hp = Text(str(player.life), fontsize=80, color=BLACK)
        hp.draw(HP_BOUNDS)
        glPopMatrix()
        del hp

    def action(self, controller):
        player = self.objects[self.client.identity]
        rx, ry = controller.rel()
        player.rx += rx
        player.ry += ry
        player.reaction -= 1
        others = self.objects.copy()
        del others[self.client.identity]
        for i, bullet in enumerate(player.bullets):
            bullet.forward()
            if abs(bullet.x) > 10000 or abs(bullet.y) > 10000:
                del player.bullets[i]
                continue
            for other in others.values():
                if self._contains(self.obj, other, bullet):
                    del player.bullets[i]
                    break
        for other in others.values():
            for i, bullet in enumerate(other.bullets):
                if self._contains(self.bullet_obj, bullet, player):
                    player.life -= 10
                    continue
        print player.life
        if controller.up:
            player.forward()
        if controller.button_a and player.reaction <= 0:
            player.bullets.append(objects.Bullet(player))
            player.reset_reaction()
        self.objects = self.client.send(player)
        return self
