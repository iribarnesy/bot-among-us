import random
import pyautogui
import time
import threading
from PIL import ImageGrab

from src.utils import SingletonMeta, KillableThread
from src.utils import FOCUS_AMONG_SCREEN, manhattan_distance
from src.vision import VisionManager, GamePhase
from src.tasks import TaskManager, TaskType, Task
from src.navigation import NavigationManager

class BrainManager(metaclass=SingletonMeta):
    def __init__(self, bot_position=None, vision_manager=None):
        self.MAX_RETRIES = 4

        self.sabotage_resolution_thread = None
        self.tasks_resolution_thread = None

        self.next_task: Task = None
        self.position = bot_position
        self.vision_manager = vision_manager

        self.events = {
            'btnReportChanged': self.on_report_btn_changed,
            'btnKillChanged': self.on_kill_btn_changed,
            'btnSecurityChanged': self.on_camera_btn_changed,
            'btnAdminChanged': self.on_admin_btn_changed,
            'btnSabotageChanged': self.on_sabotage_btn_changed,
            'gamePhaseChanged': self.on_game_phase_changed,
            'sabotageRunningChanged': self.on_sabotage_running_changed
        }

    def connect_events(self, blacklist_events=[]):
        # whitelist_events = list(filter(lambda x: x.lower() not in blacklist_events, self.events))
        whitelist_events = { key: self.events[key] for key in self.events if key not in blacklist_events }

        for event_name, handle_func in whitelist_events.items():
            self.vision_manager.event_handler.link(handle_func, event_name)
        self.events = whitelist_events

    ### On event handled

    def on_report_btn_changed(self, is_btn_report_active):
        if is_btn_report_active:
            # If we are impostor, 1/10 chance we report.
            if VisionManager().is_impostor():
                if random.random() < 0.1:
                    pyautogui.moveTo(1770,730)
                    pyautogui.click()
                    # pyautogui.press("r")
            else:
                pyautogui.moveTo(1770,730)
                pyautogui.click()
                # pyautogui.press("r")
    
    def on_kill_btn_changed(self, is_btn_kill_active):
        if is_btn_kill_active:
            pyautogui.moveTo(1540,950)
            pyautogui.click()
            #pyautogui.press("q")

    def on_camera_btn_changed(self, is_btn_security_active):
        if is_btn_security_active:
            pass
            # pyautogui.press("e")

    def on_admin_btn_changed(self, is_btn_admin_active):
        if is_btn_admin_active:
            pass
            # pyautogui.press("e")

    def on_sabotage_btn_changed(self, is_btn_sabotage_active):
        if is_btn_sabotage_active:
            pass
            # pyautogui.press("e")

    def on_game_phase_changed(self, game_phase):
        if game_phase == GamePhase.Vote:
            self.stop_tasks_resolution_thread()
            pyautogui.moveTo(337,936)
            pyautogui.click()
            pyautogui.moveTo(571,936)   
            pyautogui.click()
        elif game_phase == GamePhase.Game:
            print("Game phase : Do your tasks ! 🏃‍♂️")
            self.start_tasks_resolution_thread()

    def on_sabotage_running_changed(self, sabotage_running: TaskType):
        if sabotage_running is not None:
            print("Detected that", sabotage_running, "is running ! ☣")
            self.stop_tasks_resolution_thread()
            self.start_sabotage_resolution_thread(sabotage_running)
        else:
            if self.is_sabotage_resolution_running():
                self.stop_sabotage_resolution_thread()
            self.start_tasks_resolution_thread()
            
    ### Tasks resolution

    def start_tasks_resolution_thread(self):
        self.tasks_resolution_thread = KillableThread(name="tasks_resolution", target=self.tasks_resolution)
        self.tasks_resolution_thread.start()
    
    def tasks_resolution(self):
        self.get_nearest_task()
        while(self.next_task != None):
            print(f"Next task : {self.next_task.name}")
            BrainManager().go_and_perform(self.next_task)
            self.get_nearest_task()
        print("All tasks done ! ✅")
    
    def is_tasks_resolution_running(self):
        if self.tasks_resolution_thread is not None:
            return self.tasks_resolution_thread.is_alive()
        else:
            return False
    
    def stop_tasks_resolution_thread(self):
        if self.tasks_resolution_thread is not None:
            self.tasks_resolution_thread.kill()
            print("Terminate :", self.tasks_resolution_thread)


    ### Sabotage resolution

    def start_sabotage_resolution_thread(self, sabotage_running: TaskType):
        self.sabotage_resolution_thread = KillableThread(name="sabotage_resolution", target=self.sabotage_resolution, args=(sabotage_running,))
        self.sabotage_resolution_thread.start()
    
    def sabotage_resolution(self, sabotage_running: TaskType):
        # start thread to resolve the sabotage, stop it when it's fixed
        sabotage_task = list(filter(lambda x: x.task_type == sabotage_running, TaskManager().sabotages))[-1]
        is_task_done = False
        tries = 0
        while not is_task_done and tries < self.MAX_RETRIES:
            is_task_done = self.go_and_perform(sabotage_task)
            tries += 1
    
    def is_sabotage_resolution_running(self):
        if self.sabotage_resolution_thread is not None:
            return self.sabotage_resolution_thread.is_alive()
        else:
            return False
    
    def stop_sabotage_resolution_thread(self):
        if self.sabotage_resolution_thread is not None:
            self.sabotage_resolution_thread.kill()
            print("Terminate :", self.sabotage_resolution_thread)

    # dead emoji 👻

    ### Control methods
    
    def go_to_destination(self, destination):
        MINIMAL_DISTANCE_BEFORE_CHECK_POSITION = 25
        NUMBER_OF_ACTIONS_BEFORE_CHECK_POSITION = 10
        moving_actions = NavigationManager().get_moving_actions_to_destination(destination, self.position.find_me())
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

    def perform_task(self, task):
        want_to_read_tasks = VisionManager().want_to_read_tasks
        VisionManager().want_to_read_tasks = False
        if task.task_type != TaskType.Unlock_Manifold:
            TaskManager().start_task()
        task.solve()
        VisionManager().want_to_read_tasks = want_to_read_tasks

    def go_and_perform(self, task: Task):
        self.go_to_destination(task.location)
        if VisionManager().is_btn_use_active():
            print(f"Perform task : {task.name} 🦾")
            self.perform_task(task)
            time.sleep(1.5)
            return True
        else:
            return False


    ### Tasks methods

    def get_tasks(self):
        FOCUS_AMONG_SCREEN()
        pyautogui.press("tab")
        img = ImageGrab.grab(bbox=(0,0 ,1920,1080))
        pix = img.load()
        tasks = []
        for task in TaskManager().tasks:
            # if pix[task.indicator_location] > (190, 190, 0) and pix[task.indicator_location] < (255, 255, 80) and pix[task.indicator_location][2] < 200 and pix[task.indicator_location][1] != 17:
            if pix[task.indicator_location] > (160, 160, 67) and pix[task.indicator_location] < (255, 255, 80) and pix[task.indicator_location][2] < 200:
                tasks.append(task)
        pyautogui.press("tab")

        return tasks

    def get_nearest_task(self):
        tasks = self.get_tasks()
        if len(tasks) == 0:
            self.next_task = None
        else :
            source_coordinates = self.position.find_me()
            task_and_manhattan = [(task, manhattan_distance(source_coordinates, task.location)) for task in tasks]
            task_and_manhattan = sorted(task_and_manhattan, key=lambda task_len: task_len[1])
            for test in task_and_manhattan:
                print(test[0].name)
            self.next_task = task_and_manhattan[0][0]
        # TODO : Compute the real distance for the x nearest tasks, stock self.next_task and self.next_path.
        # task_and_len_path = [(task,len(self.get_moving_actions_to_destination(task.location, source_coordinates))) for task in tasks]
        # task_and_len_path = sorted(task_and_len_path, key=lambda task_len: task_len[1])
        # self.next_task = task_and_len_path[0][0]
        # return self.next_task
