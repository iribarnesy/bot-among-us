import random
import pyautogui
import time
import threading
import pickle
from PIL import ImageGrab
import pandas as pd
from datetime import datetime

from src.game_map import SkeldMap
from src.utils import SingletonMeta, KillableThread
from src.utils import FOCUS_AMONG_SCREEN, manhattan_distance
from src.vision import VisionManager, GamePhase
from src.tasks import TaskManager, TaskType, Task
from src.navigation import NavigationManager
from src.log import Log

DATA_FOLDER_PATH = 'src/data/'

class BrainManager(metaclass=SingletonMeta):
    def __init__(self, bot_position=None, bot_room=None, vision_manager=None):
        self.MAX_RETRIES = 4

        self.sabotage_resolution_thread = None
        self.tasks_resolution_thread = None
        self.memorize_room_thread = None
        self.time_init = time.time()

        self.next_task: Task = None
        self.position = bot_position
        self.room = bot_room
        self.vision_manager = vision_manager
        self.tasks_to_fake = None

        self.log = None
        self.sentences = []

        self.events = {
            'btnReportChanged': self.on_report_btn_changed,
            'btnKillChanged': self.on_kill_btn_changed,
            'btnSecurityChanged': self.on_camera_btn_changed,
            'btnAdminChanged': self.on_admin_btn_changed,
            'btnSabotageChanged': self.on_sabotage_btn_changed,
            'gamePhaseChanged': self.on_game_phase_changed,
            'sabotageRunningChanged': self.on_sabotage_running_changed,
            'seePeople': self.on_see_people
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
            self.stop_memorize_room_thread()
            pyautogui.moveTo(337,936)
            pyautogui.click()
            pyautogui.moveTo(571,936)   
            pyautogui.click()
        elif game_phase == GamePhase.Game:
            self.time_init = time.time()
            self.reset_log()
            print("Game phase : Do your tasks ! 🏃‍♂️")
            self.start_tasks_resolution_thread()
            print("Game phase : Memorize your rooms !") 
            self.start_memorize_room_thread()

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
        if self.vision_manager.is_impostor():
            self.tasks_resolution_thread = KillableThread(name="tasks_resolution", target=self.fake_task)
        else:
            self.tasks_resolution_thread = KillableThread(name="tasks_resolution", target=self.tasks_resolution)
        print("Start :", self.tasks_resolution_thread)            
        self.tasks_resolution_thread.start()
    
    def tasks_resolution(self):
        self.get_nearest_task()
        while(self.next_task != None):
            print(f"Next task : {self.next_task.name}")
            self.go_and_perform(self.next_task)
            self.get_nearest_task()
        print("All tasks done ! ✅")
        #Tasks are finished, we patrol then !  
        self.patrol()

    def fake_task(self):
        if self.tasks_to_fake == None :
            self.tasks_to_fake = self.get_tasks()
        while len(self.tasks_to_fake) != 0:
            task_to_fake = self.tasks_to_fake.pop(0)
            print(f"Next task : {task_to_fake.name}")
            self.go_and_fake(task_to_fake)
            print("Task faked Haha !")
            if len(self.tasks_to_fake == 0):
                self.addLog(room=None, task="J'ai fini mes tâches !", toPrint=True)
            else:
                self.addLog(room=self.room, task=task_to_fake.name, toPrint=True)
        print("All tasks Faked ! ✅")
        self.patrol()
    
    def is_tasks_resolution_running(self):
        if self.tasks_resolution_thread is not None:
            return self.tasks_resolution_thread.is_alive()
        else:
            return False
    
    def stop_tasks_resolution_thread(self):
        if self.tasks_resolution_thread is not None:
            self.tasks_resolution_thread.kill()
            print("Terminate :", self.tasks_resolution_thread)

    ### Vote methods

    def vote(self, target):
        img = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
        pix = img.load()
        lst_crewmate = [(880, 260), (880, 400), (880, 540), (880, 680), (880, 820), (1540, 260), (1540, 400), (1540, 540), (1540, 680), (1540, 820)]
        valid_button = 160
        x_pix_check_color = 530
        y_pix_check_color = 50

        if target  == "None":
            pyautogui.moveTo(337,936)
            pyautogui.click()
            pyautogui.moveTo(571,936)   
            pyautogui.click()
        else:
            for crewmate in lst_crewmate:
                if pix[crewmate][0] > 230:
                    if pix[crewmate[0] - x_pix_check_color, crewmate[1] + y_pix_check_color] == target.value:
                        pyautogui.moveTo(crewmate)
                        pyautogui.click()
                        pyautogui.moveTo(crewmate[0] - valid_button, crewmate[1])
                        pyautogui.click()
                        break

    ### Sabotage resolution

    def start_sabotage_resolution_thread(self, sabotage_running: TaskType):
        self.sabotage_resolution_thread = KillableThread(name="sabotage_resolution", target=self.sabotage_resolution, args=(sabotage_running,))
        print("Start :", self.sabotage_resolution_thread)
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

    def patrol(self):
        with open(DATA_FOLDER_PATH + 'path_patrol.pkl', 'rb') as f:
            path = pickle.load(f)

        with open(DATA_FOLDER_PATH + 'moving_actions_patrol.pkl', 'rb') as f:
            moving_actions = pickle.load(f)
        
        our_position = self.position.find_me()
        # find the closer point
        closer_point = (0,0)
        closer_indice = 0
        closer_distance = 99999
        # print("SEARCH CLOSER")
        for i in range(len(path)):
            distance = manhattan_distance(our_position, path[i])
            if distance < closer_distance:
                closer_point = path[i]
                closer_indice = i
                closer_distance = distance
        # print("Closer", closer_point)

        # Go to closer point
        self.go_to_destination_from_pos(closer_point, our_position)
        print("START PATROL")
        # Start patrol
        moving_actions_start = NavigationManager().get_moving_action_from_path(path[closer_indice:])
        self.follow_move_actions(moving_actions_start)
        # print("TRUE PATROL")
        while(True):
            self.follow_move_actions(moving_actions)

    def charge_patrol(self):
        print("Charge")
        path = []
        path.append(NavigationManager().calculate_path((1016, 130),(683, 515)))
        path.append(NavigationManager().calculate_path((683, 515),(322, 217))[1:])
        path.append(NavigationManager().calculate_path((322, 217),(197, 494))[1:])
        path.append(NavigationManager().calculate_path((197, 494),(201, 590))[1:])
        print("1")
        path.append(NavigationManager().calculate_path((201, 590),(499, 541))[1:])
        path.append(NavigationManager().calculate_path((499, 541),(374, 868))[1:])
        path.append(NavigationManager().calculate_path((374, 868),(736, 684))[1:])
        print("2")
        path.append(NavigationManager().calculate_path((736, 684),(1178, 729))[1:])
        path.append(NavigationManager().calculate_path((1178, 729),(1296, 727))[1:])
        path.append(NavigationManager().calculate_path((1296, 727),(1304, 630))[1:])
        path.append(NavigationManager().calculate_path((1304, 630), (1448, 207))[1:])
        print("3")
        path.append(NavigationManager().calculate_path((1448, 207), (1315, 475))[1:])
        path.append(NavigationManager().calculate_path((1315, 475),(1749, 531))[1:])
        path.append(NavigationManager().calculate_path((1749, 531),(1444, 873))[1:])
        print("4")
        path.append(NavigationManager().calculate_path((1444, 873),(1216, 972))[1:])
        path.append(NavigationManager().calculate_path((1216, 972),(1016, 130))[1:])
        pathFlat = [item for sublist in path for item in sublist]

        print(path)
        print("\n\n\n")
        print(pathFlat)
        print("\n\n\n")

        print("GO")
        moving_actions = NavigationManager().get_moving_action_from_path(pathFlat)
        print(moving_actions)
        print("\n\n\n")
        
        with open(DATA_FOLDER_PATH + 'moving_actions_patrol.pkl', 'wb') as f:
            pickle.dump(moving_actions, f)

        with open(DATA_FOLDER_PATH + 'path_patrol.pkl', 'wb') as f:
            pickle.dump(pathFlat, f)

    def go_to_destination_from_pos(self, destination, position):
        moving_actions = NavigationManager().get_moving_actions_to_destination(destination, position)
        self.follow_move_actions(moving_actions)

    def go_to_destination(self, destination):
        moving_actions = NavigationManager().get_moving_actions_to_destination(destination, self.position.find_me())
        self.follow_move_actions(moving_actions)

    def follow_move_actions(self,moving_actions):
        MINIMAL_DISTANCE_BEFORE_CHECK_POSITION = 15
        NUMBER_OF_ACTIONS_BEFORE_CHECK_POSITION = 10
        self.position.set_health_pos()
        nb_actions_executed = 0
        # threadStarted = False
        for moving_action in moving_actions:
            self.position.move(moving_action.distance, moving_action.direction)
            # moving_action_thread = threading.Thread(name="moving_action", 
            #     target=self.position.move, 
            #     args=(moving_action.distance, moving_action.direction,))
            # moving_action_thread.start()
            if nb_actions_executed >= NUMBER_OF_ACTIONS_BEFORE_CHECK_POSITION and moving_action.distance > MINIMAL_DISTANCE_BEFORE_CHECK_POSITION:
                # if threadStarted:
                #     findme_action_thread.join()
                # findme_action_thread = threading.Thread(name="moving_action", 
                #     target=self.position.find_me)
                # findme_action_thread.start()
                # threadStarted = True
                nb_actions_executed = 0
                self.position.find_me()
                if self.position.too_far_from_health_pos() :
                    print("On revient dans le droit chemin !")
                    self.go_to_destination((self.position.horizontal_position_healthCheck, self.position.vertical_position_healthCheck))
            # moving_action_thread.join()
            nb_actions_executed += 1

    @VisionManager.pause_vision_manager_detect_players_decorator
    @VisionManager.pause_vision_manager_read_tasks_decorator
    def perform_task(self, task: Task):
        if task.task_type != TaskType.Unlock_Manifold:
            TaskManager().start_task()
        task.solve()

    def go_and_perform(self, task: Task):
        self.go_to_destination(task.location)
        if VisionManager().is_btn_use_active():
            print(f"Perform task : {task.name} 🦾")
            self.perform_task(task)
            self.addLog(room=self.room, task=task.name, toPrint=True)
            return True
        else:
            return False

    def go_and_fake(self, task: Task):
        self.go_to_destination(task.location)
        time.sleep(task.time_to_fake)

    """ Logs methods
    """
    def start_memorize_room_thread(self):
        self.memorize_room_thread = KillableThread(name="is_new_room", target=self.is_new_room)
        print("Start :", self.memorize_room_thread)
        self.memorize_room_thread.start()


    def stop_memorize_room_thread(self):
        if self.memorize_room_thread is not None:
            self.memorize_room_thread.kill()
            print("Terminate :", self.memorize_room_thread)

    def update_room(self, write_log=True):
        for room in SkeldMap('src/img/new_walkable_small.png').room:
            if room.isIn(self.position.get_tuple_coordinates()) and room.name != self.room:
                self.room = room.name
                if write_log:
                    if not self.log.empty:
                        players = self.log["players"].iloc[-1]
                        killed = self.log["killed"].iloc[-1]
                    else :
                        players = []
                        killed = []
                    self.addLog(room=self.room, players=players, killed=killed, toPrint=True)

    def is_new_room(self, write_log=True):
        memorize = True
        while memorize: 
            self.update_room(write_log)
            

    def on_see_people(self, liste_people):
        player_alive = liste_people["players"]
        player_dead = liste_people["killed"]
        self.update_room(write_log=False)
        self.addLog(room=self.room, players=player_alive, killed=player_dead, toPrint=True)

    def addLog(self, room, players = [], killed = [], task="", toPrint = False):
        new_log = Log(room, time=(time.time() - self.time_init), players=players, killed=killed, task=task)

        if not self.log.empty:
            last_log = Log(self.log.iloc[-1]['room'], self.log.iloc[-1]['time'], self.log.iloc[-1]['players'], self.log.iloc[-1]['killed'], self.log.iloc[-1]['task'])
            if not last_log.equal(new_log):
                self.log = self.log.append(new_log.log_to_dataframe())
                if(toPrint):
                    print(new_log)
        else:
            self.log = self.log.append(new_log.log_to_dataframe())
            if(toPrint):
                    print(new_log)

    def clear_logs(self):
        """ Remove the rows where a player disappear and appear again
        """
        indexes_sure_to_drop = []
        indexes_that_may_be_dropped = []
        index_to_match_for_ubiquity = 0
        for i in range(2, len(self.log)):
            current_line = self.log.iloc[i]
            line_to_match_for_ubiquity = self.log.iloc[index_to_match_for_ubiquity]
            
            a_column_changed = Log.a_column_changed(line_to_match_for_ubiquity, current_line, ['room', 'task'])
            a_player_appeared = Log.player_appeared(line_to_match_for_ubiquity, current_line)
            if a_column_changed or a_player_appeared:
                index_to_match_for_ubiquity = i
                indexes_that_may_be_dropped = []
            elif Log.player_disappeared(line_to_match_for_ubiquity, current_line):
                indexes_that_may_be_dropped.append(i)
            else:
                indexes_that_may_be_dropped.append(index_to_match_for_ubiquity)
                indexes_sure_to_drop += indexes_that_may_be_dropped
                index_to_match_for_ubiquity = i
                indexes_that_may_be_dropped = []
        self.log = self.log.drop(indexes_sure_to_drop)
        return self.log
        
    def generate_sentences(self):
        self.clear_logs()
        self.sentences = [Log(*self.log.iloc[i]).sentence(Log(*self.log.iloc[i + 1])) for i in range(len(self.log) - 1)]
        return self.sentences

    def write_logs_to_file(self, filename=datetime.today().strftime("%Y-%m-%d_%Hh%Mm%Ss")):
        path = f"{DATA_FOLDER_PATH}{filename}.logs.csv"
        self.log.to_csv(path, index=False, mode="a", header=True)
    
    def write_sentences_to_file(self, filename=datetime.today().strftime("%Y-%m-%d_%Hh%Mm%Ss")):
        path = f"{DATA_FOLDER_PATH}{filename}.sentences.txt"
        with open(path, 'a', encoding="utf-8") as f:
            f.write("\n".join(self.sentences))


    """ Mais mdr c'est quoi c'te fonction d'la mort x))"""
    def sentence_from2Logs(self, log1: Log, log2: Log):
        print("\n")
        lst_people_arrive = []
        lst_people_leave = []
        lst_people_just_die = []

        lst_people_present = []
        task_done = ""

        retour = ""

        # Dans le cas ou on est dans la même salle
        if log1.room == log2.room:
            retour = "J'étais " + log1.room

            # Dans le cas ou on a effectué une tâche
            if log1.task != "" or log2.task != "":
                if log1.task != "":
                    task_done = log1.task
                    lst_people_present = log2.players.copy()
                else :
                    task_done = log2.task
                    lst_people_present = log1.players.copy()
                # Construction de la chaine retour
                retour += ", j'ai fais la tâche " + task_done + " et y'avait "
                for player  in lst_people_present:
                    retour += player + " et "
                retour = retour[0:len(retour) - len(" et ")] + " dans la pièce"
            
            # Dans les cas les plus globaux
            else:
                for player in log1.players:
                    if player in log2.players:
                        lst_people_present.append(player)
                    else:
                        lst_people_leave.append(player)
                for player in log2.players:
                    if player in log1.players and player not in lst_people_present:
                        lst_people_arrive.append(player)
                if log1.killed != log2.killed:
                    for kill in log2.killed:
                        if kill not in log1.killed:
                            lst_people_just_die.append(kill)
                # Construction de la chaine retour
                if len(lst_people_present) != 0:
                    retour += " avec "
                    for player  in lst_people_present:
                        retour += player + " et "
                    retour = retour[0:len(retour) - len(" et ")]

                if len(lst_people_leave) != 0 or len(lst_people_arrive) != 0 or len(lst_people_just_die) != 0:
                    retour += ", j'ai vu "
                    if len(lst_people_arrive) != 0:
                        for player  in lst_people_arrive:
                            retour += player + " et "
                        retour = retour[0:len(retour) - len(" et ")] + " arriver, "
                    if len(lst_people_leave) != 0:
                        for player  in lst_people_leave:
                            retour += player + " et "
                        retour = retour[0:len(retour) - len(" et ")] + " partir, "
                    if len(lst_people_just_die) != 0:
                        for player  in lst_people_just_die:
                            retour += player + " et "
                        retour = retour[0:len(retour) - len(" et ")] + " qui vient juste de mourir."

        else:
            for player in log1.players:
                if player in log2.players:
                    lst_people_present.append(player)
                else:
                    lst_people_leave.append(player)
            for player in log2.players:
                if player not in log1.players and player not in lst_people_leave:
                    lst_people_leave.append(player)


            if log1.room == "Couloir":
                retour += "Je suis entré " + log2.room
            elif log2.room == "Couloir":
                retour += "Je suis sorti de " + log1.room
            if len(lst_people_leave) != 0:
                retour += ", j'ai croisé "
                for player  in lst_people_leave:
                    retour += player + " et "
                retour = retour[0:len(retour) - len(" et ")]
            if len(lst_people_present) != 0:
                retour += " j'étais avec "
                for player  in lst_people_present:
                    retour += player + " et "
                retour = retour[0:len(retour) - len(" et ")]
            if len(log1.killed) != 0 or len(log2.killed) != 0 :
                retour += " et j'ai vu le cadavre de "
                for kill in log1.killed:
                    retour += kill + " et "
                for kill in log2.killed:
                    retour += kill + " et "
                retour = retour[0:len(retour) - len(" et ")]
        
        print(retour)

    def reset_logs(self):
        self.log.drop(columns=["room","time","players","killed", "task"], inplace=True)
        self.log = pd.DataFrame(columns=["room","time","players","killed", "task"])
        self.addLog(room=None, task="Début de round", toPrint=True)

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
            #for test in task_and_manhattan:
                #print(test[0].name)
            self.next_task = task_and_manhattan[0][0]
        # TODO : Compute the real distance for the x nearest tasks, stock self.next_task and self.next_path.
        # task_and_len_path = [(task,len(self.get_moving_actions_to_destination(task.location, source_coordinates))) for task in tasks]
        # task_and_len_path = sorted(task_and_len_path, key=lambda task_len: task_len[1])
        # self.next_task = task_and_len_path[0][0]
        # return self.next_task

    def road_to_somebody(self, point_destination):
        X_ECRAN = 1920
        Y_ECRAN = 1080
        NB_SPECIAL = 4.61

        x_dest_min, y_dest_min, x_dest_max, y_dest_max = point_destination
        x_dest = int((x_dest_max + x_dest_min) / 2)
        y_dest = int((y_dest_max + y_dest_min) / 2)
        x_init = X_ECRAN / 2
        y_init = Y_ECRAN / 2

        action1 = {"value" : 0, "name": ""}
        action2 = {"value" : 0, "name": ""}

        while(x_init != x_dest or y_init != y_dest):

            if(x_init > x_dest):
                # Vers en haut à gauche
                if(y_init > y_dest):
                    action = "left-up"
                    x_dest = x_dest +1
                    y_dest = y_dest +1
                # Vers en bas à gauche
                elif(y_init < y_dest):
                    action = "left-down"
                    x_dest = x_dest +1
                    y_dest = y_dest -1
                # Vers la gauche
                else:
                    action = "left"
                    x_dest = x_dest +1

            elif(x_init < x_dest):
                # Vers en haut à droite
                if(y_init > y_dest):
                    action = "right-up"
                    y_dest = y_dest +1
                    x_dest = x_dest -1
                # Vers en bas à droite
                elif(y_init < y_dest):
                    action = "right-down"
                    x_dest = x_dest -1
                    y_dest = y_dest -1
                # Vers la droite
                else:
                    action = "right"
                    x_dest = x_dest -1
            else:
                # Vers le bas
                if(y_init < y_dest):
                    action = "down"
                    y_dest = y_dest -1
                # Vers le bas
                elif(y_init > y_dest):
                    action = "up"
                    y_dest = y_dest +1

            if action1["name"] == "":
                action1["name"] = action
                action1["value"] = 1
            elif action1["name"] == action:
                action1["value"] += 1
            else:
                if action2["name"] == "":
                    action2["name"] = action
                    action2["value"] = 1
                elif action2["name"] == action:
                    action2["value"] += 1


        action1["value"] = int(action1["value"] / NB_SPECIAL)
        action2["value"] = int(action2["value"] / NB_SPECIAL)

        self.position.move(action1["value"], action1["name"])
        self.position.move(action2["value"], action2["name"])



        