from image import Image

import gutil

BLACK = (30,30,30,255)

WHITE = (255,255,255,255)

class Text(Image):

    def __init__(self, text, fontsize = 24, color = (0,0,0,0), font = None, antialias = 1):
        texttexture = gutil.loadText(text, fontsize, color, font, antialias)
        self.texture = texttexture[0]
        self.width = texttexture[1]
        self.height = texttexture[2]
        self.texture_width = texttexture[3]
        self.texture_height = texttexture[4]
        self.displayList = gutil.createTexDL(self.texture, self.texture_width, self.texture_height)
