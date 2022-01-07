from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from config import TILESIZE
from typing import Tuple, List


class Pathfinder:
    def __init__(self,matrix: List):
        self.matrix = matrix
        self.grid = Grid(matrix = matrix)
        # pathfinding
        self.path = []

    def get_path(self, pos: Tuple, start: Tuple) -> None: 
        self.pos = pos
        #start
        start_x, start_y = start
        start = self.grid.node(start_x, start_y)
        #end
        end_x, end_y = self.pos[0] // TILESIZE, self.pos[1] // TILESIZE
        end = self.grid.node(end_x, end_y)
        # path
        finder = AStarFinder(diagonal_movement = DiagonalMovement.always)
        self.path,_ = finder.find_path(start, end, self.grid)
        self.grid.cleanup()
        return self.path
    
    def empty_path(self):
        self.path = []