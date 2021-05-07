import time
import numpy as np
import pandas as pd
import cv2
from PIL import ImageGrab, Image
import pytesseract
import math
from enum import Enum
from shapely.geometry import Polygon, Point

import src.utils as utils
from src.enums.texts import TasksTexts


class Log:
    def __init__(self,room, players=[], killed=[], time = time.time(), task=""):
        self.room = room # Cafet
        self.time = time # t secode
        self.players = players # [yellow ...]
        self.killed = killed # [pink ...]
        self.task = task


    def __repr__(self):
        retour = "(LOG) " + str(self.time) + " - " + str(self.room)
        if self.task != "":
            retour = retour + " - Task done : " + self.task
        if len(self.players) > 0:
            retour = retour + " - Players {"
            for player in self.players:
                retour = retour + player + ", "
            retour = retour [0:len(retour)-2] + "}"
        if len(self.killed) > 0:
            retour = retour + " - Killed {"
            for kill in self.killed:
                retour = retour + kill + ", "
            retour = retour[0:len(retour)-2]+ "}"

        return retour

    def log_to_dataframe(self):
        d = {'room': [self.room], 'time': [self.time], 'players': [self.players], 'killed': [self.killed], 'task': [self.task]}
        df = pd.DataFrame(data=d)
        return df
    
    def equal(self, Log):
        if Log.room == self.room and len(Log.players) == len(self.players) and len(Log.killed) == len(self.killed) and Log.task == self.task:
            for player in self.players:
                if(player not in Log.players):
                    return False
            for kill in self.killed:
                if(kill not in Log.killed):
                    return False
            return True
        else:
            return False