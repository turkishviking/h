import pygame
import time
from PIL import Image


def get_frames(filename):
    image = Image.open(filename)
    pal = image.getpalette()
    base_palette = []
    for i in range(0, len(pal), 3):
        rgb = pal[i:i + 3]
        base_palette.append(rgb)

    all_tiles = []
    try:
        while 1:
            if not image.tile:
                image.seek(0)
            if image.tile:
                all_tiles.append(image.tile[0][3][0])
            image.seek(image.tell() + 1)
    except EOFError:
        image.seek(0)

    all_tiles = tuple(set(all_tiles))

    frames = []
    try:
        while 1:
            try:
                duration = image.info["duration"]
            except:
                duration = 100

            duration *= .001  # convert to milliseconds!


            cons = False

            x0, y0, x1, y1 = (0, 0) + image.size
            if image.tile:
                tile = image.tile
            else:
                image.seek(0)
                tile = image.tile
            if len(tile) > 0:
                x0, y0, x1, y1 = tile[0][1]

            if all_tiles:
                if all_tiles in ((6,), (7,)):
                    cons = True
                    pal = image.getpalette()
                    palette = []
                    for i in range(0, len(pal), 3):
                        rgb = pal[i:i + 3]
                        palette.append(rgb)
                elif all_tiles in ((7, 8), (8, 7)):
                    pal = image.getpalette()
                    palette = []
                    for i in range(0, len(pal), 3):
                        rgb = pal[i:i + 3]
                        palette.append(rgb)
                else:
                    palette = base_palette
            else:
                palette = base_palette

            pi = pygame.image.fromstring(image.tobytes(), image.size, image.mode)

            if "transparency" in image.info:
                pi.set_colorkey(image.info["transparency"])
            pi2 = pygame.Surface(image.size, pygame.SRCALPHA)
            if cons:
                for i in frames:
                    pi2.blit(i[0], (0, 0))
            pi2.blit(pi, (x0, y0), (x0, y0, x1 - x0, y1 - y0))

            frames.append([pi2, duration])
            image.seek(image.tell() + 1)
    except EOFError:
        pass

    del frames[0]
    return frames