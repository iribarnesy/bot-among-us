from PIL import Image
import numpy as np
import copy

from src.utils import SingletonMeta

class NavigationManager(metaclass=SingletonMeta):
    def __init__(self, map_img_path):
        self.map_img_path = map_img_path
        self.map_matrix = []

    def init_matrix(self):
        img_map_pix = Image.open(self.map_img_path)
        img_map = np.array(img_map_pix)

        self.map_matrix = np.count_nonzero(img_map, axis=2)
        self.map_matrix = np.where(self.map_matrix > 1, 1, 0)

    def calculate_path(self, source_coordinates, target_coordinates):
        pass