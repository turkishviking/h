import pyglet
from pyglet2d import Shape
import os
import random
import time
import math



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
        self.rectangle = None
        self.ellipse = None
        self.circle = None
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
        centerX = self.sprite.width/2. + posX
        centerY = self.sprite.height/2.+ posY
        radius = self.sprite.width/1.7

        circleCoord = self.getAllCircleCoords(centerX, centerY, radius, 80)
        self.circle = Shape.regular_polygon((200, 200), 40, 20)
        self.circle.color = (255,0,255)
        self.rectangle = Shape.rectangle([[100, 100], [300, 300]])
        self.rectangle = self.rectangle  - self.circle
        self.rectangle.color = (255,255,0)
        self.lastTime = self.now()



    # This function gets just one pair of coordinates based on the angle theta
    def getCircleCoord(self, theta, x_center, y_center, radius):
        x = radius * math.cos(theta) + x_center
        y = radius * math.sin(theta) + y_center
        return (x, y)

    # This function gets all the pairs of coordinates
    def getAllCircleCoords(self, x_center, y_center, radius, n_points):
        thetas = [i / n_points * math.tau for i in range(n_points)]
        circle_coords = [self.getCircleCoord(theta, x_center, y_center, radius) for theta in thetas]
        return circle_coords



    def on_draw(self):
        self.clear()
        self.sprite.draw()
        self.rectangle.draw()
        self.circle.draw()
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







