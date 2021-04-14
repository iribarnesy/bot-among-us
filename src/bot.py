import time
from PIL import ImageGrab
import numpy as np
import cv2
import pyautogui
import pytesseract
from pytesseract import Output
from itertools import groupby
from typing import List, Tuple
import math

import src.navigate as navigate
import src.tasks as tasks
from src.tasks import TaskType
import src.game_map as game_map
from src.position import Position, Directions


class MovingAction:
    """ Represents a moving action.
    For example : "Go top for 5 pixels" will be Action(direction="top", distance=5)
    """
    def __init__(self, direction, distance: int):
        self.direction: str = direction
        self.distance: int = distance
        
        # Distances over the diags are longer
        # if self.direction in ['top-right', 'bottom-right', 'bottom-left', 'top-left']:
        #     self.distance = distance * math.sqrt(2)
        # else:
        #     self.distance = distance

    def __repr__(self):
        return f"{self.distance:.2f} x {self.direction}"


class Bot:
    def __init__(self, map_img_path='src/img/WalkableMesh_resize_small.png'):
        self.name = "Le bot"
        self.game_map = game_map.SkeldMap(map_img_path)
        self.position = Position()

    def menu(self):
        print("What would you like to do?")
        print("[1] Run Bot")
        print("[2] Solve Tasks")
        print("[3] Navigate to Tasks")
        print("[4] Find me")

        option = int(input('options:'))

        if(option == 1):
            self.startup()
        if(option == 2):
            self.game_map.taskManager.prompt_task()
        if(option == 3):
            prompt_message_task_number = 'task number in :\n'+"\n".join(str(t) for t in self.game_map.taskManager.tasks)
            navigate.pathfinding(int(input(prompt_message_task_number)))
        # if(option == 4):
        #     self.find_me()

    def startup(self):
        time.sleep(2)
        self.scale_percent = 100 # percent of original size
        self.width = int(1920 * self.scale_percent / 100)
        self.height = int(1080 * self.scale_percent / 100)
        self.dim = (self.width, self.height)
        self.select_screen()
        self.read_map()

    def read_map(self):
        while True:
            pyautogui.press("tab")
            img = ImageGrab.grab(bbox=(0,0 ,1920,1080))
            pix = img.load()
            task = None
            for t in self.game_map.taskManager.tasks:
                if pix[t.location] > (190, 190, 0) and pix[t.location] < (255, 255, 80) and pix[t.location][2] < 200 and pix[t.location][1] != 17:
                    print(t.name)
                    print(pix[t.location])
                    task = t
            if task is not None:
                result = navigate.pathfinding(self.game_map.taskManager.tasks.index(task))
                pyautogui.press("tab")
                if result == 1:
                    self.perform_task(task)

    def select_screen(self):
        pyautogui.click(int(self.width/2), int(self.height/2))

    def perform_task(self, task):
        if task.task_type != TaskType.Unlock_Manifold:
            self.game_map.taskManager.start_task()
        task.solve()


    def get_vector_direction(self, source_coordinates, target_coordinates):
        """ Substract the two coordinates to get the direction of the vector
        Return a vector_direction, for example (1,1) for the top-right direction
        """
        return tuple(target_coordinates[axis] - source_coordinates[axis] for axis in range(len(source_coordinates)))
    
    def get_action_str(self, vector_direction):
        vector_directions_to_actions_str = {
            (0,-1): Directions.UP,
            (1,-1): Directions.RIGHT_UP,
            (1,0): Directions.RIGHT,
            (1,1): Directions.RIGHT_DOWN,
            (0,1): Directions.DOWN,
            (-1,1): Directions.LEFT_DOWN,
            (-1,0): Directions.LEFT,
            (-1,-1): Directions.LEFT_UP
        }
        return vector_directions_to_actions_str[vector_direction]

    def get_moving_actions_from_vector_directions(self, vector_directions):
        """ Get the moving actions by grouping along the same vector_directions and aggregating by counting
        """
        return [MovingAction(self.get_action_str(vector_direction),sum(1 for _ in group)) for vector_direction, group in groupby(vector_directions)]

    def get_moving_actions_to_destination(self, destination):
        """ Calculate the path between the current position and the destination given and 
        generate a list of moving actions to get to the destination.
        For example, to go right and then top-right it will be : [MovingAction('right',5), MovingAction('top-right', 8.5)]
        """
        self.position.find_me()
        factor = 4
        self.position.horizontal_position = self.position.horizontal_position // factor
        self.position.vertical_position = self.position.vertical_position // factor
        print(self.position.get_tuple_coordinates())
        path, _ = self.game_map.navigationManager.calculate_path(self.position.get_tuple_coordinates(), destination)
        vector_directions = []
        for target_coordinates in path[1:]:
            vector_directions.append(self.get_vector_direction(self.position.get_tuple_coordinates(), target_coordinates))
            self.position.horizontal_position = target_coordinates[0]
            self.position.vertical_position = target_coordinates[1]
        
        actions = self.get_moving_actions_from_vector_directions(vector_directions)
        return actions

    def execute_actions(self, destination):
        actions = self.get_moving_actions_to_destination(destination)
        factor = 4
        for action in actions:
            self.position.move(action.distance * factor,action.direction)


if __name__ == '__main__':
    b = Bot()
    b.menu()