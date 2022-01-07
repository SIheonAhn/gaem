from csv import reader
import pygame
from config import TILESIZE
from typing import List

def import_csv_layout(path: str) -> List:
    """ Takes a .cvs file, converts it into a list
    
    Args:
        path: the file path to the target .cvs file
    
    Returns:
        terrain_map: a matrix of values that corresponds to the values in the .cvs file
    """
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter = ',') # delimiter is what seperates each data point in the csv file
        for row in level:
            terrain_map.append(list(row))
    
    return terrain_map

def import_cut_graphic(path: str) -> List:
    """ Slices tilemap image into 32*32 images then converts those images into surfaces

    Args:
        path: the file path to the target graphic. The image is a tilemap with all of the assets

    Returns:
        cut_tiles: a list of pygame surfaces with 32*32 images on them
    """
    surface = pygame.image.load(path).convert() # converting makes it faster for some reason
    tile_num_x = int(surface.get_size()[0] / TILESIZE)
    tile_num_y = int(surface.get_size()[1] / TILESIZE)
    
    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * TILESIZE
            y = row * TILESIZE
            new_surf = pygame.Surface((TILESIZE, TILESIZE)).convert_alpha()
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, TILESIZE, TILESIZE))
            cut_tiles.append(new_surf)

    return cut_tiles