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
import random
import threading

import src.navigate as navigate
import src.tasks as tasks
from src.tasks import TaskType, Task
import src.game_map as game_map
from src.position import Position, Directions
from src.utils import FOCUS_AMONG_SCREEN
from src.vision import VisionManager, GamePhase

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
        self.vision_manager = VisionManager()
        self.position = Position()
        self.next_task: Task = None
        # event
        VisionManager().event_handler.link(self.reportKill, 'btnReportChanged')
        VisionManager().event_handler.link(self.kill, 'btnKillChanged')
        VisionManager().event_handler.link(self.camera, 'btnSecurityChanged')
        VisionManager().event_handler.link(self.admin, 'btnAdminChanged')
        VisionManager().event_handler.link(self.sabotage, 'btnSabotageChanged')
        VisionManager().event_handler.link(self.vote, 'gamePhaseChanged')

    def menu(self):
        print("What would you like to do?")
        print("[1] Run Bot")
        print("[2] Solve Tasks")
        print("[3] Navigate to Tasks")
        print("[4] Find me")

        option = int(input('options:'))

        if(option == 1):
            self.run()
        if(option == 2):
            self.game_map.task_manager.prompt_task()
        if(option == 3):
            prompt_message_task_number = 'task number in :\n'+"\n".join(str(t) for t in self.game_map.task_manager.tasks)
            navigate.pathfinding(int(input(prompt_message_task_number)))
        # if(option == 4):
        #     self.find_me()

    def run(self):
        print("GET !")
        self.get_nearest_task()
        while(self.next_task != None):
            print("NEAREST :")
            print(self.next_task.name)
            self.go_to_destination(self.next_task.location)
            print("PERFORM !")
            self.perform_task(self.next_task)
            time.sleep(1.5)
            self.get_nearest_task()
        print("FIN LOL")


    def get_tasks(self):
        FOCUS_AMONG_SCREEN()
        pyautogui.press("tab")
        time.sleep(0.1)
        img = ImageGrab.grab(bbox=(0,0 ,1920,1080))
        pix = img.load()
        tasks = []
        for task in self.game_map.task_manager.tasks:
            
            # if pix[task.indicator_location] > (190, 190, 0) and pix[task.indicator_location] < (255, 255, 80) and pix[task.indicator_location][2] < 200 and pix[task.indicator_location][1] != 17:
            if pix[task.indicator_location] > (160, 160, 67) and pix[task.indicator_location] < (255, 255, 80) and pix[task.indicator_location][2] < 200:
                tasks.append(task)
        pyautogui.press("tab")

        return tasks

    def manhattan_distance(self,source,target):
        distance = abs(source[0]-target[0]) + abs(source[1]-target[1])
        return distance

    def get_nearest_task(self):
        tasks = self.get_tasks()
        if len(tasks) == 0:
            self.next_task = None
        else :
            source_coordinates = self.position.find_me()
            task_and_manhattan = [(task,self.manhattan_distance(source_coordinates, task.location)) for task in tasks]
            task_and_manhattan = sorted(task_and_manhattan, key=lambda task_len: task_len[1])
            for test in task_and_manhattan:
                print(test[0].name)
            self.next_task = task_and_manhattan[0][0]
        # TODO : Compute the real distance for the x nearest tasks, stock self.next_task and self.next_path.
        # task_and_len_path = [(task,len(self.get_moving_actions_to_destination(task.location, source_coordinates))) for task in tasks]
        # task_and_len_path = sorted(task_and_len_path, key=lambda task_len: task_len[1])
        # self.next_task = task_and_len_path[0][0]
        # return self.next_task


    def read_map(self):
        while True:
            pyautogui.press("tab")
            img = ImageGrab.grab(bbox=(0,0 ,1920,1080))
            pix = img.load()
            task = None
            for t in self.game_map.task_manager.tasks:
                if pix[t.indicator_location] > (190, 190, 0) and pix[t.indicator_location] < (255, 255, 80) and pix[t.indicator_location][2] < 200 and pix[t.indicator_location][1] != 17:
                    print(t.name)
                    print(pix[t.indicator_location])
                    task = t
            if task is not None:
                result = navigate.pathfinding(self.game_map.task_manager.tasks.index(task))
                pyautogui.press("tab")
                if result == 1:
                    self.perform_task(task)

    def perform_task(self, task):
        if task.task_type != TaskType.Unlock_Manifold:
            self.game_map.task_manager.start_task()
        task.solve()


    def get_vector_direction(self, source_coordinates, target_coordinates):
        """ Substract the two coordinates to get the direction of the vector
        Return a vector_direction, for example (1,1) for the top-right direction
        """
        return tuple(target_coordinates[axis] - source_coordinates[axis] for axis in range(len(source_coordinates)))
    
    def get_action_str(self, vector_direction):
        scale = self.game_map.navigation_manager.scale 
        vector_directions_to_actions_str = {
            (0       , -1*scale): Directions.UP,
            (1*scale , -1*scale): Directions.RIGHT_UP,
            (1*scale , 0       ): Directions.RIGHT,
            (1*scale , 1*scale ): Directions.RIGHT_DOWN,
            (0       , 1*scale ): Directions.DOWN,
            (-1*scale, 1*scale ): Directions.LEFT_DOWN,
            (-1*scale, 0       ): Directions.LEFT,
            (-1*scale, -1*scale): Directions.LEFT_UP
        }
        return vector_directions_to_actions_str[vector_direction]

    def get_moving_actions_from_vector_directions(self, vector_directions):
        """ Get the moving actions by grouping along the same vector_directions and aggregating by counting
        """
        scale = self.game_map.navigation_manager.scale
        return [MovingAction(self.get_action_str(vector_direction),sum(scale for _ in group)) for vector_direction, group in groupby(vector_directions)]

    def get_moving_actions_to_destination(self, destination, source_coordinates=None):
        """ Calculate the path between the current position and the destination given and 
        generate a list of moving actions to get to the destination.
        For example, to go right and then top-right it will be : [MovingAction('right',5), MovingAction('top-right', 8.5)]
        """
        if not source_coordinates:
            source_coordinates = self.position.find_me()
        path = self.game_map.navigation_manager.calculate_path(source_coordinates, destination)
        if len(path) == 0:
            print("Didn't find a path between source and target ! 🐾")
            return []
        vector_directions = []
        source_coordinates = path[0]
        for target_coordinates in path[1:]:
            vector_directions.append(self.get_vector_direction(source_coordinates, target_coordinates))
            source_coordinates = target_coordinates
        
        actions = self.get_moving_actions_from_vector_directions(vector_directions)
        return actions

    def go_to_destination(self, destination):
        MINIMAL_DISTANCE_BEFORE_CHECK_POSITION = 25
        NUMBER_OF_ACTIONS_BEFORE_CHECK_POSITION = 10
        moving_actions = self.get_moving_actions_to_destination(destination)
        nb_actions_executed = 0
        for moving_action in moving_actions:
            moving_action_thread = threading.Thread(name="moving_action", 
                target=self.position.move, 
                args=(moving_action.distance, moving_action.direction,))
            moving_action_thread.start()
            if nb_actions_executed >= NUMBER_OF_ACTIONS_BEFORE_CHECK_POSITION and moving_action.distance > MINIMAL_DISTANCE_BEFORE_CHECK_POSITION:
                self.position.find_me()
                nb_actions_executed = 0
            moving_action_thread.join()
            nb_actions_executed += 1

    def reportKill(self, is_btn_report_active):
        if is_btn_report_active:
            # If we are impostor, 1/10 chance we report.
            if self.vision_manager.is_impostor():
                if random.random() < 0.1:
                    pyautogui.moveTo(1770,730)
                    pyautogui.click()
                    # pyautogui.press("r")
            else:
                pyautogui.moveTo(1770,730)
                pyautogui.click()
                # pyautogui.press("r")
    
    def kill(self, is_btn_kill_active):
        if is_btn_kill_active:
            pyautogui.moveTo(1540,950)
            pyautogui.click()
            #pyautogui.press("q")

    def camera(self, is_btn_security_active):
        if is_btn_security_active:
            pyautogui.press("e")

    
    def admin(self, is_btn_admin_active):
        if is_btn_admin_active:
            pyautogui.press("e")

    def sabotage(self, is_btn_sabotage_active):
        if is_btn_sabotage_active:
            pyautogui.press("e")

    
    def vote(self, is_vote_time):
        if is_vote_time == GamePhase.Vote:
            pyautogui.moveTo(337,936)
            pyautogui.click()
            pyautogui.moveTo(571,936)   
            pyautogui.click()
    

if __name__ == '__main__':
    b = Bot()
    b.menu()
