from config import *

class Camera:
    def __init__(self, map):
        self.camera = (0, 0)
        self.map = map
        self.mapwidth = len(map[0]) * TILESIZE
        self.mapheight = len(map) * TILESIZE
    def apply(self, entity):
        return entity.rect.move(self.camera)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)
        # limit scrolling to map size (BROKEN)
        #x = min( 0, x) # left
        #y = min(0, y) # top
        #x = max(-(self.mapwidth- WIDTH), x) # right
        #y = max(-(self.mapheight - HEIGHT), y) # bottom
        self.camera = (x, y)