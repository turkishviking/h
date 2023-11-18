import pygame as pg

class Rectangle(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.original_image = pg.Surface((100, 100))
        self.original_image.fill((255, 0, 0))
        self.image = self.original_image
        self.rect = self.image.get_rect()

    def set_rounded(self, roundness):
        size = self.original_image.get_size()
        self.rect_image = pg.Surface(size, pg.SRCALPHA)
        pg.draw.rect(self.rect_image, (255, 255, 255), (0, 0, *size), border_radius=roundness)

        self.image = self.original_image.copy().convert_alpha()
        self.image.blit(self.rect_image, (0, 0), None, pg.BLEND_RGBA_MIN)

pg.init()
window = pg.display.set_mode((200, 200))

rect_object = Rectangle()
rect_object.set_rounded(30)
rect_object.rect.center = window.get_rect().center
group = pg.sprite.Group(rect_object)

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    window.fill((128, 128, 128))
    group.draw(window)
    pg.display.flip()