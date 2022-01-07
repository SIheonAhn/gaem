from typing import Dict, List
from support import import_csv_layout, import_cut_graphic
from config import TILESIZE
from sprites import WallTile, FloorTile


class Level:
    """ Uses support.py to format and import tilemap images, creates a matrix for the pathfinder,and adds sprites to their respective
    groups based on the supplied .cvs file 
    """
    def __init__(self, level_data: Dict, overworld) -> None: # ""
        self.overworld = overworld

        #terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.create_tile_group(terrain_layout, 'terrain')
        self.create_pathfinding_matrix(terrain_layout)
        # shadow setup (broken)
        shadows_layout = import_csv_layout(level_data['shadows'])
        self.create_tile_group(shadows_layout, "shadows")
    
    def create_tile_group(self, layout: List, type: str) -> None:
        """ Takes the list converted from the .cvs file, then creates sprite object based on the information
        
        Args: 
            layout: a list that contains map information converted using import_csv_layout() 
            type: a string that detemines which layer to use. Different layers can have the same values for different blocks, so this
            distiction is important
        
        Returns:
            None
        """
        for row_index, row in enumerate(layout):
            for col_index, tile in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if type == "terrain":
                    terrain_tile_list = import_cut_graphic("assets/terrain/terrain.png")
                    tile_surface = terrain_tile_list[int(tile)]
                    if tile != "-1" and tile != "21":
                        WallTile(x, y, tile_surface, self.overworld)
                    elif tile == "21":
                        FloorTile(x, y, tile_surface, self.overworld)
                
                elif type == "shadows":
                    shadow_tile_list = import_cut_graphic("assets/terrain/terrain.png")
                    tile_surface = shadow_tile_list[int(tile)]
                    FloorTile( x, y, tile_surface, self.overworld)


    def create_pathfinding_matrix(self, layout: List):
        """ Takes the list with all of the walls then converts it into a matrix (0 is a wall, 1 isn't) for the pathfinder.py. 
        Stores it into overworld.map_matrix

        Args:
            layout: a list that contains map information converted using import_csv_layout() 
        
        Returns:
            None
        """
        pathfinding_matrix = []
        for row in layout:
            pathfinding_row = []
            for tile in row:
                # Matrix generation for pathfinding
                if tile != "-1" and tile != "21":
                    pathfinding_row.append("0")
                else:
                    pathfinding_row.append("1")
            pathfinding_matrix.append(pathfinding_row)
        
        self.overworld.map_matrix = pathfinding_matrix


    def run(self):
        pass