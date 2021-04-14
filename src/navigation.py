from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from PIL import Image
import numpy as np
import copy

from src.utils import SingletonMeta

class NavigationManager(metaclass=SingletonMeta):
    def __init__(self, map_img_path):
        self.map_img_path = map_img_path
        self.map_matrix = None
        self.original_height = 1080
        self.original_width = 1920
        self.height = 0
        self.width = 0

    def init_matrix(self):
        img_map_pix = Image.open(self.map_img_path)    

        img_map = np.array(img_map_pix)
        self.height = img_map.shape[0]
        self.width = img_map.shape[1]

        self.map_matrix = np.count_nonzero(img_map, axis=2)
        self.map_matrix = np.where(self.map_matrix > 1, 1, 0)

    def calculate_path(self, source_coordinates, target_coordinates):
        """ calculate a path between a start point and an end point of a matrix
        input : self.map_matrix
        output : path
        """
        if self.map_matrix is None:
            self.init_matrix()
        
        grid = Grid(matrix=self.map_matrix)
        start = grid.node(*source_coordinates)
        end = grid.node(*target_coordinates)
        #finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)
        path, runs = finder.find_path(start, end, grid)

        return path, runs

    def path_to_grid(self, path, must_print=True, result_file_path=None):
        """ Create a representation of a given path in the map_matrix.
        's', 'e' represents respectively the start and end points. 'x' is the path and '#' is an obstacle
        ex : 
            +---+
            |sx |
            | #x|
            |  e|
            +---+
        """
        grid = Grid(matrix=self.map_matrix)
        if(len(path) > 0):
            grid_str = grid.grid_str(path=path, start=grid.node(*path[0]), end=grid.node(*path[-1]))
            if result_file_path:
                with open(result_file_path, "w") as result_file:
                    result_file.write(grid_str)
            if must_print:
                print(grid_str)
            return grid_str
        else:
            if must_print:
                print("-- No path possible --")
            return None

    def convert_for_realmap(self, position):
        scale = self.original_height / self.height
        print(str(self.original_height) + " / " + str(self.height))
        print(scale)
        pos_x, pos_y = position

        return int(pos_x*scale), int(pos_y*scale)

    def convert_for_minimap(self, position):
        scale = self.original_height / self.height
        pos_x, pos_y = position

        return int(pos_x/scale), int(pos_y/scale)




