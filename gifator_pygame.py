import pygame
import pygame.gfxdraw
from pygame_animatedgif import AnimatedGifSprite
import os, random, time

############################################
"""       PARAMETERS GO HERE <3          """
############################################
FOLDER = "/home/charlie/Pictures/h"
SIZE = 800, 600
BORDER_RADIUS = 200
############################################




############################################
class Rectangle(pygame.sprite.Sprite):
    def __init__(self, animation, ratio):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.Surface(SIZE)
        self.original_image.fill((255, 0, 0))
        self.scaling_factor = ratio*0.6

        self.image = self.textureImage = self.original_image
        self.rect = self.image.get_rect()
        self.frames = animation.get_frames(animation.filename)
        self.currentFrame = 0

    def set_rounded(self, roundness):
        size = self.original_image.get_size()
        self.rect_image = pygame.Surface(SIZE, pygame.SRCALPHA)
        pygame.draw.rect(self.rect_image, (255, 255, 255), (0, 0, *size), border_radius=roundness)

        self.image = self.original_image.copy().convert_alpha()
        self.image.blit(self.rect_image, (0, 0), None, pygame.BLEND_RGBA_MIN)

    def update(self, *args, **kwargs):
        self.rect = self.image.get_rect()
        charImage = self.frames[self.currentFrame][0]
        self.currentFrame += 1
        if self.currentFrame == len(self.frames):
            self.currentFrame = 0

        charImage = pygame.transform.scale(charImage, self.original_image.get_size())
        charImage = charImage.convert()
        self.original_image.blit(charImage, self.rect)

        self.image = self.original_image.copy().convert_alpha()
        self.image.blit(self.rect_image, (0, 0), None, pygame.BLEND_RGBA_MIN)

class Gifator:

    def __init__(self):
        self.gifList = os.listdir(FOLDER)
        self.gif = None
        self.animation = None
        self.lastTime = None
        self.rect = None
        self.spriteGroup = None
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        self.getRandomGif()


    def getRandomGif(self):
        self.gif = os.path.join(FOLDER, random.choice(self.gifList))
        self.animation = AnimatedGifSprite((0, 0), self.gif)

        #resize
        H_ratio = min(self.animation.get_height(), SIZE[1]) / max(self.animation.get_height(), SIZE[1])
        W_ratio = min(self.animation.get_width(), SIZE[0]) / max(self.animation.get_width(), SIZE[0])
        ratio = max(H_ratio, W_ratio)
        self.animation.scale(ratio)

        self.animation.rect.x = SIZE[0]/2. - self.animation.get_width()*ratio/2.
        self.animation.rect.y = SIZE[1]/2. - self.animation.get_height()*ratio/2.

        self.rect = Rectangle(self.animation, ratio)
        self.rect.set_rounded(BORDER_RADIUS)
        self.rect.rect.center = self.screen.get_rect().center


        self.spriteGroup = pygame.sprite.Group()
        #self.spriteGroup.add(self.animation)
        self.spriteGroup.add(self.rect)


        self.lastTime = self.now()

    def deltaTime(self):
        return self.now() - self.lastTime

    def now(self):
        return time.time()

    def play(self):
        #self.animation.play()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            if self.deltaTime() > 2:
                self.getRandomGif()


            self.screen.fill((0, 255, 0))

            self.spriteGroup.update(self.screen)
            self.spriteGroup.draw(self.screen)



            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    gifator = Gifator()
    gifator.play()