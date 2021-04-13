import time
from PIL import ImageGrab
import numpy as np
import cv2
import pyautogui
import pytesseract
from pytesseract import Output
from itertools import groupby

import src.navigate as navigate
import src.tasks as tasks
from src.tasks import TaskType
import src.game_map as game_map


class Bot:
    def __init__(self):
        self.name = "Le bot"
        self.tasks = None
        self.game_map = game_map.SkeldMap('src/img/WalkableMesh_resize_small.png')

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
            self.game_map.prompt_task()
        if(option == 3):
            prompt_message_task_number = 'task number in :\n'+"\n".join(str(t) for t in self.game_map.tasks)
            navigate.pathfinding(int(input(prompt_message_task_number)))
        if(option == 4):
            self.find_me()

    def find_me(self):
        c = pyautogui.locateOnScreen('src/img/map_character.png', grayscale=True, confidence=.65)
        pyautogui.moveTo(c)
        return c

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
            for t in self.game_map.tasks:
                if pix[t.location] > (190, 190, 0) and pix[t.location] < (255, 255, 80) and pix[t.location][2] < 200 and pix[t.location][1] != 17:
                    print(t.name)
                    print(pix[t.location])
                    task = t
            if task is not None:
                result = navigate.pathfinding(self.game_map.tasks.index(task))
                pyautogui.press("tab")
                if result == 1:
                    self.perform_task(task)

    def select_screen(self):
        pyautogui.click(int(self.width/2), int(self.height/2))

    def perform_task(self, task):
        if task.task_type != TaskType.Unlock_Manifold:
            self.game_map.start_task()
        task.solve()

    
    def get_direction(self, source_coordinate, target_coordinate):
        direction = []

        for axis in range(0, len(source_coordinate)):
            
            direction.append(target_coordinate[axis] - source_coordinate[axis])

        return tuple(direction)
        

    def get_direction_and_distance(self, directions):
        directions_and_distances = [(value,sum(1 for _ in group)) for value, group in groupby(directions)]
        
        return directions_and_distances

    
    def get_action(self, direction):
        # I think it's better if we can do with a dict 

        if direction == (0,-1) :
            action = 'top'
        elif direction == (1,-1) : 
            action = 'top-right'
        elif direction == (1,0) : 
            action = 'right'
        elif direction == (1,1) : 
            action = 'bottom-right'
        elif direction == (0,1) : 
            action = 'bottom'
        elif direction == (-1,1) : 
            action = 'bottom-left'
        elif direction == (-1,0) : 
            action = 'left'
        elif direction == (-1,-1) : 
            action = 'top-left'
        
        return action


    def get_action_and_distance(self, directions_and_distances):
        
        return [(self.get_action(direction), distance) for direction, distance in directions_and_distances]
        

    def get_actions_to_destination(self, destination):
        source_coordinate = (60,216)
        path, _ = self.game_map.navigationManager.calculate_path(source_coordinate, destination)
        directions = []
        for target_coordinate in path[1:]:
            directions.append(self.get_direction(source_coordinate, target_coordinate))
            source_coordinate =target_coordinate
        
        directions_and_distances = self.get_direction_and_distance(directions)
        action_and_distance = self.get_action_and_distance(directions_and_distances)

        return action_and_distance
        # return list de direction et de distance  [Action]

    b.menu()