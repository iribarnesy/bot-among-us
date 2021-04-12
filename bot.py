import time
from PIL import ImageGrab
import numpy as np
import cv2
import pyautogui
import pytesseract
import navigate
import tasks
from tasks import TaskType
import game_map
from pytesseract import Output


class Bot:
    def __init__(self):
        self.name = "Le bot"
        self.tasks = None
        self.game_map = game_map.SkeldMap()

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
        c = pyautogui.locateOnScreen('map_character.png', grayscale=True, confidence=.65)
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

if __name__ == '__main__':
    b = Bot()
    b.menu()