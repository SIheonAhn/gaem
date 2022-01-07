import pygame as pg
from config import *
from sprites import *
from pathfinder import *
from game import Game

g = Game()
g.new()
while g.running:
    g.run()

pg.quit()