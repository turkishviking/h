import pygame

screen = pygame.display.set_mode((800, 600))
sp = pygame.sprite.Group()
sp.update(screen)
while True:
    sp = pygame.sprite.Group()
    sp.update(screen)
    pygame.event.pump()
    pygame.display.flip()