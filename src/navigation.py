from src.utils import SingletonMeta

class NavigationManager(metaclass=SingletonMeta):
    def __init__(self, map_img_path):
        self.map_img_path = map_img_path
        self.map_matrix = []

    def init_matrix(self):
        pass

    def calculate_path(self, source_coordinates, target_coordinates):
        pass