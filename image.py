from OpenGL.GL import *
import gutil
import os

class Image:
    def __init__(self, texname=None):
        filename = os.path.join('data', texname)
        filename += ".png"

        self.texture, self.width, self.height = gutil.loadImage(filename)
        self.displayList = gutil.createTexDL(self.texture, self.width, self.height)
     
    def __del__(self):
        if self.texture != None:
            gutil.delTexture(self.texture)
            self.texture = None
        if self.displayList != None:
            gutil.delDL(self.displayList)
            self.displayList = None

    def draw(self, bounds, color=(1,1,1,1), rotation=0, rotationCenter=None):
        glColor4fv(color)

        pos = (bounds[0], bounds[1])

        width = bounds[2]

        height = bounds[3]

        if pos:
            glLoadIdentity()
            glTranslate(pos[0],pos[1],0)

         
        if rotation != 0:
                if rotationCenter == None:
                    rotationCenter = (self.width / 2, self.height / 2)
                (w,h) = rotationCenter
                glTranslate(rotationCenter[0],rotationCenter[1],0)
                glRotate(rotation,0,0,-1)
                glTranslate(-rotationCenter[0],-rotationCenter[1],0)
             
        if width or height:
            if not width:
                width = self.width
            elif not height:
                height = self.height

            glScalef(width/(self.width*1.0), height/(self.height*1.0), 1.0)

        glCallList(self.displayList)

