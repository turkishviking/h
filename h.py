import pygame
import pygame.gfxdraw
from h_lib import get_frames
import os, random, time
from threading import Thread, Lock

############################################
"""       PARAMETERS GO HERE <3          """
############################################
FOLDER = "/home/charlie/Pictures/h"
SIZE = 800, 600
BORDER_RADIUS = 150
TIME_TO_CHANGE_GIF = 2 #secondes!
FPS = 60.
############################################

pygame.display.set_caption('Hachinator')
Icon = pygame.image.load('h.jpg')


############################################
class Rectangle(pygame.sprite.Sprite):
    def __init__(self, gif):
        pygame.sprite.Sprite.__init__(self)
        self.frames = get_frames(gif)

        # resize
        h = self.frames[1][0].get_height()
        w = self.frames[1][0].get_width()
        H_ratio = min(h, SIZE[1]) / max(h, SIZE[1])
        W_ratio = min(w, SIZE[0]) / max(w, SIZE[0])
        ratio = min(H_ratio, W_ratio)*0.92

        self.posx = (SIZE[0] / 2. - w *ratio/ 2.)
        self.posy = (SIZE[1] / 2. - h *ratio/ 2.)


        self.original_image = pygame.Surface((w*ratio,h*ratio))
        self.original_image.fill((255, 0, 0))


        self.image = self.textureImage = self.original_image
        self.rect = self.image.get_rect()

        self.currentFrame = 0

        self.scaling_factor = 1
        self.ptime = time.time()

    def set_rounded(self, roundness):
        size = self.original_image.get_size()
        self.rect_image = pygame.Surface(SIZE, pygame.SRCALPHA)
        pygame.draw.rect(self.rect_image, (255, 255, 255), (0, 0, *size), border_radius=roundness)

        self.image = self.original_image.copy().convert_alpha()
        self.image.blit(self.rect_image, (0, 0), None, pygame.BLEND_RGBA_MIN)

    def get_height(self):
        return self.image.get_height()

    def get_width(self):
        return self.image.get_width()

    def get_size(self):
        return self.image.size

    def scale(self, scale_factor):
        self.scaling_factor = scale_factor

    def update(self, *args, **kwargs):
        if time.time() - self.ptime > self.frames[self.currentFrame][1]:

            self.ptime = time.time()

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

            if self.scaling_factor != 1:
                self.image = pygame.transform.scale(self.image,
                                                    (int(self.image.get_rect().width * self.scaling_factor),
                                                     int(self.image.get_rect().height * self.scaling_factor)))

            self.rect.x = self.posx
            self.rect.y = self.posy

class Gifator:

    def __init__(self):
        self.gifList = os.listdir(FOLDER)
        self.gif = None
        self.lastTime = time.time()
        self.spriteGroup = None
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)

        self.gif = os.path.join(FOLDER, random.choice(self.gifList))
        self.rect = Rectangle(self.gif)
        self.rect.set_rounded(BORDER_RADIUS)
        #self.rect.rect.center = self.screen.get_rect().center

        self.spriteGroup = pygame.sprite.Group()
        self.thread = Thread(target=self.getNextGif)
        self.nextGif = None
        self.thread.start()
        self.lock = Lock()
        self.clock = pygame.time.Clock()

    def getRandomGif(self):
        with self.lock:
            if self.nextGif is not None:
                self.rect.kill()
                self.rect = self.nextGif
        if self.rect is not None:
            self.spriteGroup = pygame.sprite.Group()
            self.spriteGroup.add(self.rect)

            self.thread = Thread(target=self.getNextGif)
            self.thread.start()

            self.lastTime = self.now()
        else:
            time.sleep(1) #wait for first iteration


    def deltaTime(self):
        return self.now() - self.lastTime

    def now(self):
        return time.time()

    def play(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            if self.deltaTime() > TIME_TO_CHANGE_GIF:
                self.getRandomGif()


            self.screen.fill((0, 255, 0))

            self.spriteGroup.update(self.screen)
            self.spriteGroup.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

    def getNextGif(self):
        gif = os.path.join(FOLDER, random.choice(self.gifList))
        nextGif = Rectangle(gif)
        nextGif.set_rounded(BORDER_RADIUS)

        with self.lock:
            self.nextGif = nextGif


if __name__ == "__main__":
    pygame.init()
    gifator = Gifator()
    gifator.play()