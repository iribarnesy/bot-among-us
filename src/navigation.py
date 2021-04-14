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
        self.scale = None

        self.init_matrix()

    def init_matrix(self):
        OBSTACLE_WEIGHT_VALUE = 0
        BEST_PATH_WEIGHT_VALUE = 1
        WALKABLE_WEIGHT_VALUE = 2

        def get_weight(non_zeros_values):
            map_non_zeros_values_to_weight_values = {
                4: BEST_PATH_WEIGHT_VALUE,
                2: WALKABLE_WEIGHT_VALUE,
                1: OBSTACLE_WEIGHT_VALUE
            }
            return map_non_zeros_values_to_weight_values[non_zeros_values]
        
        img_map_pix = Image.open(self.map_img_path)    
        img_map = np.array(img_map_pix)
        self.scale = self.original_width // img_map.shape[1]

        self.map_matrix = np.count_nonzero(img_map, axis=2)
        v_get_weight = np.vectorize(get_weight)
        self.map_matrix = np.array(list(map(v_get_weight, self.map_matrix)))

    def calculate_path(self, source_coordinates, target_coordinates):
        """ calculate a path between a start point and an end point of a matrix
        input : coordinates sized for the realmap
        output : path with coordinates sized for realmap
        """
        source_coordinates, target_coordinates = self.convert_for_minimap(source_coordinates), self.convert_for_minimap(target_coordinates)
        grid = Grid(matrix=self.map_matrix)
        start = grid.node(*source_coordinates)
        end = grid.node(*target_coordinates)
        #finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)
        path, _ = finder.find_path(start, end, grid)

        return [self.convert_for_realmap(coordinates) for coordinates in path]

    def path_to_grid(self, path, must_print=True, result_file_path=None):
        """ Create a representation of a given path (sized for realmap) in the map_matrix.
        's', 'e' represents respectively the start and end points. 'x' is the path and '#' is an obstacle
        ex : 
            +---+
            |sx |
            | #x|
            |  e|
            +---+
        """
        grid = Grid(matrix=self.map_matrix)
        path = [self.convert_for_minimap(coordinates) for coordinates in path]
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
        pos_x, pos_y = position
        return int(pos_x*self.scale), int(pos_y*self.scale)

    def convert_for_minimap(self, position):
        pos_x, pos_y = position
        return int(pos_x/self.scale), int(pos_y/self.scale)




