import pygame as pg
from config import *
from pathfinder import * 

# Character Class
class Character(pg.sprite.Sprite):
    def __init__(self, game, pos: Tuple, sprite_list):
        self.game = game
        super().__init__(sprite_list)
        self.rect = self.image.get_rect(center = pos)
        # player movement
        self.pos = self.rect.center
        self.speed = 8 # Player and enemy movespeed
        self.moving = False
        self.coord_list = []
        self.clear_data()
        self.pathfinder = Pathfinder(game.map_matrix)

    def set_path(self, pos):
        self.path = self.pathfinder.get_path(pos, self.get_coord())
        self.distance = len(self.path)
        self.create_coord_list() 

    def get_coord(self):
        col = self.rect.centerx // TILESIZE
        row = self.rect.centery // TILESIZE
        return(col, row)

    def get_distance(self):
        return self.distance
  
    def create_coord_list(self):
        if self.path:
            self.coord_list = []
            for point in self.path:
                x = (point[0] * TILESIZE) + TILESIZE/2
                y = (point[1] * TILESIZE) + TILESIZE/2
                self.coord_list.append((x, y))
    
    def clear_data(self):
        self.path = []
        self.coord_list = []
        self.current_cell = 0
        self.moving = False
        self.distance = 0

    def move(self):
        start = pg.math.Vector2(self.rect.center)
        if self.coord_list and self.distance > self.current_cell:
            self.moving = True
            end = pg.math.Vector2(self.coord_list[self.current_cell])
            startx = start[0]
            starty = start[1]
            endx = end[0]
            endy = end[1]

            if starty - endy > self.speed/2:
                self.rect.centery -= self.speed # move up
            elif endy - starty > self.speed/2:
                self.rect.centery += self.speed # move down
            
            if startx - endx > self.speed/2:
                self.rect.centerx -= self.speed # move left
            elif endx - startx > self.speed/2:
                self.rect.centerx += self.speed # move right

            if -self.speed/2-0.1 < (end-start)[0] < self.speed/2+0.1 and -self.speed/2-0.1 < (end-start)[1] < self.speed/2+0.1:
                if self.distance > self.current_cell:
                    self.current_cell += 1
                    
                if self.distance == self.current_cell:
                    self.rect.center = self.coord_list[self.current_cell - 1]
                    self.clear_data()
            
            
    def update(self):
        self.move()

    
class Player(Character):
    def __init__(self, game, pos: Tuple):
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill((128, 105, 200))
        super().__init__(game, pos, game.playersprite)
        

class Enemy(Character):
    def __init__(self, game, pos: Tuple):
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill((245, 40, 40))
        super().__init__(game, pos, game.enemysprites)
    
    def move(self):
        start = pg.math.Vector2(self.rect.center)
        if self.coord_list and self.distance > self.current_cell:
            self.set_path(game.player.coord_list[1])
            self.moving = True
            end = pg.math.Vector2(self.coord_list[self.current_cell])
            startx = start[0]
            starty = start[1]
            endx = end[0]
            endy = end[1]

            if starty - endy > self.speed/2:
                self.rect.centery -= self.speed # move up
            elif endy - starty > self.speed/2:
                self.rect.centery += self.speed # move down
            
            if startx - endx > self.speed/2:
                self.rect.centerx -= self.speed # move left
            elif endx - startx > self.speed/2:
                self.rect.centerx += self.speed # move right

            if -self.speed/2-0.1 < (end-start)[0] < self.speed/2+0.1 and -self.speed/2-0.1 < (end-start)[1] < self.speed/2+0.1:
                if self.distance > self.current_cell:
                    self.current_cell += 1
                    
                if self.distance == self.current_cell:
                    self.rect.center = self.coord_list[self.current_cell - 1]
                    self.clear_data()

class StaticTile(pg.sprite.Sprite):
    def __init__(self, x, y, surface, sprite_list):
        super().__init__(sprite_list)
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y

class WallTile(StaticTile):
    def __init__(self, x, y, surface, game):
        super().__init__(x, y, surface, game.wallsprites) #whoho!

class FloorTile(StaticTile):
    def __init__(self, x, y, surface, game):
        super().__init__(x, y, surface, game.floorsprites)

class Shadow(StaticTile):
   def __init__(self, x, y, surface, game):
        super().__init__(x, y, surface, game.shadowsprites)