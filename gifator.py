import pyglet
from pyglet import shapes
import os
import random
import time



############################################
"""       PARAMETERS GO HERE <3          """
############################################
FOLDER = "/home/charlie/Pictures/h"
SIZE = 800, 600
TIME_TO_CHAGE_GIF = 2 #secondes!
############################################




############################################
pyglet.resource.path = [FOLDER]
pyglet.resource.reindex()

#win = pyglet.window.Window()

class Window(pyglet.window.Window):
    def __init__(self):
        super(Window, self).__init__()

        self.gifList = os.listdir(FOLDER)
        self.gif = None
        self.animation = None
        self.sprite = None
        self.lastTime = None
        self.rect = None
        self.ellipse = None
        self.batch = pyglet.graphics.Batch()
        self.set_size(*SIZE)
        self.getRandomGif()

    def getRandomGif(self):
        self.gif = random.choice(self.gifList)
        self.animation = pyglet.resource.animation(self.gif)
        self.sprite = pyglet.sprite.Sprite(self.animation)


        #resize
        H_ratio = min(self.sprite.height, SIZE[1]) / max(self.sprite.height, SIZE[1])
        W_ratio = min(self.sprite.width, SIZE[0]) / max(self.sprite.width, SIZE[0])
        self.sprite.scale_x = W_ratio
        self.sprite.scale_y = H_ratio

        posX = SIZE[0]/2. - self.sprite.width/2.
        posY = SIZE[1]/2. - self.sprite.height/2.

        self.sprite.x = posX
        self.sprite.y = posY

        #round Corner

        self.ellipse = shapes.Ellipse(self.sprite.width/2. + posX, self.sprite.height/2.+posY,
                                      self.sprite.width/1.7, self.sprite.height/1.7,
                                      color=(255, 22, 20), batch=self.batch)

        self.rectangle = shapes.Rectangle(self.sprite.width / 2. + posX, self.sprite.height / 2. + posY,
                                      self.sprite.width / 1.7, self.sprite.height / 1.7,
                                      color=(255, 22, 20), batch=self.batch)


        self.lastTime = self.now()


    def on_draw(self):
        self.clear()
        #self.ellipse = self.rectangle - self.ellipse
        self.sprite.draw()
        #self.ellipse.draw()
        if self.deltaTime() > TIME_TO_CHAGE_GIF:
            self.getRandomGif()

    def deltaTime(self):
        return self.now() - self.lastTime

    def now(self):
        return time.time()

if __name__ == '__main__':
    window = Window()
    pyglet.gl.glClearColor(0, 255, 0, 255)
    pyglet.app.run()

