import pygame
import pygame.gfxdraw
from pygame_animatedgif import AnimatedGifSprite
import os, random, time

############################################
"""       PARAMETERS GO HERE <3          """
############################################
FOLDER = "/home/charlie/Pictures/h"
SIZE = 800, 600
############################################




############################################


class Gifator:

    def __init__(self):
        self.gifList = os.listdir(FOLDER)
        self.gif = None
        self.animation = None
        self.lastTime = None
        self.rect = None
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        self.getRandomGif()


    def getRandomGif(self):
        self.gif = os.path.join(FOLDER, random.choice(self.gifList))
        self.animation = AnimatedGifSprite((50, 50), self.gif)

        #resize
        H_ratio = min(self.animation.get_height(), SIZE[1]) / max(self.animation.get_height(), SIZE[1])
        W_ratio = min(self.animation.get_width(), SIZE[0]) / max(self.animation.get_width(), SIZE[0])
        ratio = max(H_ratio, W_ratio)
        self.animation.scale(W_ratio)
        self.animation.x = SIZE[0]/2. - self.animation.get_width()/2.
        self.animation.y = SIZE[1]/2. - self.animation.get_height()/2.

        """
        self.sprite.scale_x = W_ratio
        self.sprite.scale_y = H_ratio

        """

        #round Corner
        #size = self.sprite.width
        #self.rect = pyglet.Surface(600,600, pyglet.SRCALPHA)
        #pg.draw.rect(self.rect_image, (255, 255, 255), (0, 0, *size), border_radius=roundness)

        self.lastTime = self.now()

    def deltaTime(self):
        return self.now() - self.lastTime

    def now(self):
        return time.time()

    def play(self):
        self.animation.play()
        sprite_group = pygame.sprite.Group()
        sprite_group.add(self.animation)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            if self.deltaTime() > 2:
                self.getRandomGif()
                sprite_group = pygame.sprite.Group()
                sprite_group.add(self.animation)

            self.screen.fill((0, 255, 0))
            sprite_group.update(self.screen)
            sprite_group.draw(self.screen)
            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    gifator = Gifator()
    gifator.play()