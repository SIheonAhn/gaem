import pygame as pg
from config import *
from sprites import *
from pathfinder import *
from cameramovement import *
from level import Level
from game_data import level_0

class Game: #overworld

    def __init__(self):
        pg.init()
        # pg.mixer.init()
        flags = pg.FULLSCREEN
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), vsync=1)
        pg.display.set_caption("RPG_Game")
        self.clock = pg.time.Clock()
        self.running = True
        self.abspos = (0, 0)

    def load_data(self):
        self.map_matrix = []
        Level(level_0, self)
        self.mouseimage = pg.image.load("assets/cursor.png").convert_alpha()

    def new(self):
        pg.mouse.set_visible(False)
        
        # creating sprite groups
        self.shadowsprites = pg.sprite.Group()
        self.enemysprites = pg.sprite.Group()
        self.wallsprites = pg.sprite.Group()
        self.playersprite = pg.sprite.GroupSingle()
        self.floorsprites = pg.sprite.Group()

        self.load_data()
        self.player = Player(self, (100, 100))
        self.enemy = Enemy(self, (300, 300))
        
        self.camera = Camera(self.map_matrix)
        
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            
    def update(self):
        self.playersprite.update()
        self.enemysprites.update()
        self.wallsprites.update()
        self.shadowsprites.update()
        self.camera.update(self.player)
    
    def events(self):
        for event in pg.event.get():
            self.mousepos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False
            
            if event.type == pg.MOUSEBUTTONDOWN:
                if not(self.player.moving):
                    self.getabspos(self.mousepos, self.player)
                    self.player.set_path(self.abspos)

    def draw_active_cell(self): # draws the tile that the user is hovering over
        mouse_pos = pg.mouse.get_pos()
        x = mouse_pos[0] // 32
        y = mouse_pos[1] // 32
        mouse = pg.Surface((TILESIZE, TILESIZE), pg.SRCALPHA)
        mouse.fill((30, 30, 30, 100))
        self.screen.blit(mouse, (x * TILESIZE, y * TILESIZE))

    def draw(self):
        self.screen.fill((70, 70, 70))
    
        for sprite in self.floorsprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        if not self.player.moving:
            self.draw_active_cell()

        for sprite in self.wallsprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        
        for sprite in self.playersprite:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.enemysprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            
        for sprite in self.shadowsprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        self.screen.blit(self.mouseimage, self.mousepos)
        
        pg.display.flip()

    def getabspos(self, cursorpos, target):
        x = target.rect.x - int(WIDTH / 2)
        y = target.rect.y - int(HEIGHT / 2)
        absposx = x + cursorpos[0]
        absposy = y + cursorpos[1]
        self.abspos = (absposx, absposy)

    def show_start_screen(self):
        pass