import time
import numpy as np
import cv2
from PIL import ImageGrab, Image
import pytesseract
import math
from enum import Enum
from shapely.geometry import Polygon, Point

import src.utils as utils
from src.enums.texts import TasksTexts


class Room:
    def __init__(self, name, place):
        self.name = name
        self.place = place

    
    def __repr__(self):
        return f"{self.name} : {self.place.centroid}"
    
    def isIn(self, position):
        point = Point(position)
        return self.place.contains(point)

        