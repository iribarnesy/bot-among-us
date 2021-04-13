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
        self.map_matrix = []
        self.origine_height = 1080
        self.origine_width = 1920
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
        
        grid = Grid(matrix=self.map_matrix)
        start = grid.node(*source_coordinates)
        end = grid.node(*target_coordinates)
        #finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)
        path, runs = finder.find_path(start, end, grid)

        return path, runs

    def print_path(self, path):
        grid = Grid(matrix=self.map_matrix)
        if(len(path) > 0):
            print(grid.grid_str(path=path, start=grid.node(*path[0]), end=grid.node(*path[-1])))
        else:
            print("-- No path possible --")

    def convert_for_realmap(self, position):
        scale = self.origine_height / self.height
        print(str(self.origine_height) + " / " + str(self.height))
        print(scale)
        pos_x, pos_y = position

        return int(pos_x*scale), int(pos_y*scale)

    def convert_for_minimap(self, position):
        scale = self.origine_height / self.height
        pos_x, pos_y = position

        return int(pos_x/scale), int(pos_y/scale)




