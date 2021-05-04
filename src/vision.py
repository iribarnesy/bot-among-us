from enum import Enum
import time
import numpy as np
import cv2.cv2 as cv
from PIL import ImageGrab, Image
import pyautogui
from eventhandler import EventHandler
from typing import Tuple
import math 

from src.enums.pixels import Colors, PixelPositions, PixelRegions
from src.enums.images import ImagesPath
from src.enums.texts import TasksTexts
from src.tasks import TaskType
from src.utils import draw_boxes
from src.utils import check_image, check_color, check_red, check_pixel_color
from src.utils import open_tasks_tab, close_tasks_tab, flatten, is_in_text
from src.utils import KillableThread, SingletonMeta
from src.players_recognition.players_detector import PlayersDetector
from src.utils import get_player_color, dominant_color

class GamePhase(Enum):
    Game = "game"
    Vote = "vote"
    Lobby = "lobby"

class VisionManager(metaclass=SingletonMeta):
    def __init__(self, 
                 want_to_read_tasks=True,
                 debug_mode=False):
        self.takeScreen = True
        self.vision_screen = None
        self.vision_screen_transformed = None
        self.debug_mode = debug_mode

        self.vision_thread: KillableThread = None

        self.read_tasks_thread: KillableThread = None
        self.want_to_read_tasks = want_to_read_tasks
        self.tasks_text = None
    
        self.detect_players_thread: KillableThread = None
        self.detector = PlayersDetector()

        self.memorize_players_thread: KillableThread = None
        self.last_log = None
        
        self.game_phase: GamePhase = None
        self._is_impostor = None
        self._is_btn_use_active = None
        self._is_btn_report_active = None
        self._is_btn_kill_active = None
        self._is_btn_vent_active = None
        self._is_btn_sabotage_active = None
        self._is_btn_admin_active = None
        self._is_btn_security_active = None
        self._is_sabotage_running = False
        self.sabotage_running = None

        self.SECONDS_BETWEEN_EACH_SCREEN = 0
        self.MAX_ITERATIONS_FOR_THREAD = 60
        self.event_handler = EventHandler('gamePhaseChanged', 'btnUseChanged', 'btnReportChanged', 'btnKillChanged',
                                         'btnVentChanged', 'btnSabotageChanged', 'btnAdminChanged', 'btnSecurityChanged', 
                                         'tasksTabChanged', 'sabotageRunningChanged', 'updateRoom', 'seePeople')
        self.event_handler.link(self.is_sabotage_running, 'tasksTabChanged')

    """ Global vision thread
    """
    def start_vision_loop(self):
        if not self.is_vision_looping():
            self.vision_thread = KillableThread(name="compute_screen", target=self.compute_screen)
            self.vision_thread.start()
        print("memorize players thread")
        self.memorize_players_thread = KillableThread(name="memorize_players", target=self.memorize_players)
        self.memorize_players_thread.start()

    def compute_screen(self):
        if self.debug_mode:
            cv.namedWindow('DEMO')
        for _ in range(self.MAX_ITERATIONS_FOR_THREAD):
            self.vision_screen = np.array(pyautogui.screenshot())
            self.get_game_phase()
            self.is_btn_report_active()
            self.is_btn_admin_active()
            self.is_btn_security_active()
            # self.is_btn_use_active()
            if self.want_to_read_tasks and not self.is_read_tasks_running():
                self.start_read_tasks()
                
            if self.is_impostor():
                self.is_btn_kill_active()
                # self.is_btn_sabotage_active()
                # self.is_btn_vent_active()
            
            self.start_detect_players()
            
            if self.debug_mode:
                if self.vision_screen_transformed is not None:
                    im = cv.resize(self.vision_screen_transformed, (960, 540))
                else:
                    im = cv.resize(self.vision_screen, (960, 540))
                    im = cv.cvtColor(im, cv.COLOR_BGR2RGB)
                cv.imshow('DEMO', im)
                cv.waitKey(1)

            time.sleep(self.SECONDS_BETWEEN_EACH_SCREEN)
        if self.debug_mode:
            cv.destroyAllWindows()
    
    
    def memorize_players(self):
        print("memorize_players")
        for _ in range(self.MAX_ITERATIONS_FOR_THREAD):
            self.is_see_people()

    
    def get_region(self, coordinates):
        region = [coordinates[1], coordinates[0]]
        width = math.sqrt( ((coordinates[1]-coordinates[1])**2)+((coordinates[0]-coordinates[2])**2) )
        height = math.sqrt( ((coordinates[1]-coordinates[3])**2)+((coordinates[0]-coordinates[0])**2) )

        region.append(int(width))
        region.append(int(height))

        return region
    
    def is_see_people(self):
        self.vision_screen = pyautogui.screenshot()
        # retour IA object détection : liste de liste de coordonnées [ymin%ecran, xmin%ecran, ymax%ecran, xmax%ecran] 
        # IL FAUDRAT DONC MULTIPLI PAR 1920*1080
        retour = [[477,919,597,995],[803,1218,868,1305]]
        # url_photo = "src/players_recognition/positive/" + retour.split(' ',1)[0]
        # coord = retour.split(' ',1)[1].split(' ')
        # count_players = 0
        data = {"players":[],"killed":[]}
        # while count_players < int(coord[0]):
        for player in retour:
            # actual_player_box = (int(coord[count_players*4 +2]), int(coord[count_players*4 +1]), int(coord[count_players*4 +4]), int(coord[count_players*4 +3]))
            # Define Color
            region = self.get_region(player)
            color = get_player_color((player[1], player[0]), (player[3], player[2]))
            if color == "WHITE_PLAYER":
                continue
            # Check if is death
            # print(color)
            is_dead = pyautogui.locateOnScreen('./src/img/dead_body.jpg', region=region, grayscale=True, confidence=.65)
            if is_dead:
                data["killed"].append(color)
            else:
                data["players"].append(color)
            # count_players = count_players +1
        # print(data)
        # PROBLEME ICI SI ON RESTE AVEC LES AUTRES EN CHANGEANT DE SALLE
        if self.last_log != data:
            self.event_handler.fire('seePeople', data)
            self.last_log = data

    def is_vision_looping(self):
        if self.vision_thread is not None:
            return self.vision_thread.is_alive()
        else:
            return False

    def stop_vision_loop(self):
        self.vision_thread.kill()
        print("Terminate :", self.vision_thread)
        self.memorize_players_thread.kill()
        print("Terminate :", self.memorize_players_thread)
        self.stop_read_tasks()
        self.stop_detect_players()

    """ Detection of the players
    """
    def start_detect_players(self):
        if not self.is_detect_players_running():
            self.detect_players_thread = KillableThread(name="detect_players", target=self.detect_players)
            print("Start:", self.detect_players_thread)
            self.detect_players_thread.start()

    def detect_players(self, min_confidence_threshold=0.6):
        screenshot_np = np.array(pyautogui.screenshot())
        detections = self.detector.detect_from_np_array(screenshot_np)
        boxes = detections['detection_boxes'][0].numpy()
        scores = detections['detection_scores'][0].numpy()
        # classes = detections['detection_classes'][0].numpy().astype(np.uint32)
        good_boxes = boxes[scores > min_confidence_threshold]
        # draw the detection results onto the original image
        if self.debug_mode:
            print(f"Found {len(good_boxes)} player(s)")
            self.vision_screen_transformed = draw_boxes(good_boxes, screenshot_np)

    def is_detect_players_running(self):
        if self.detect_players_thread is not None:
            return self.detect_players_thread.is_alive()
        else:
            return False

    def stop_detect_players(self):
        if self.detect_players_thread is not None:
            self.detect_players_thread.kill()
            print("Terminate :", self.detect_players_thread)

    """ Read the tasks tab
    """
    def start_read_tasks(self):
        if not self.is_read_tasks_running():
            self.read_tasks_thread = KillableThread(name="read_tasks", target=self.read_tasks)
            self.read_tasks_thread.start()

    def read_tasks(self):
        open_tasks_tab()
        tasks_tab_img = ImageGrab.grab(bbox=(flatten(PixelRegions.TASKS_TAB.value)))
        close_tasks_tab()
        tasks_tab_img.save(ImagesPath.TASKS_TAB_SCREEN.value, "png")
        result = self.detect_text(ImagesPath.TASKS_TAB_SCREEN.value).description
        if result != self.tasks_text:
            self.tasks_text = result
            self.event_handler.fire('tasksTabChanged', result)
        return self.tasks_text

    def is_read_tasks_running(self):
        if self.read_tasks_thread is not None:
            return self.read_tasks_thread.is_alive()
        else:
            return False

    def stop_read_tasks(self):
        if self.read_tasks_thread is not None:
            self.read_tasks_thread.kill()
            print("Terminate :", self.read_tasks_thread)

    def detect_text(self, path):
        """Detects text in the file."""
        from google.cloud import vision
        import io
        client = vision.ImageAnnotatorClient()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        # pylint: disable=no-member
        response = client.text_detection(image=image)
        texts = response.text_annotations

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        return texts[0]

    """ Other events
    """
    def get_game_phase(self):
        is_vote_phase = check_image(r"src\img\skip_vote.PNG")
        if is_vote_phase:
            result = GamePhase.Vote   
        else:
            result = GamePhase.Game
        if result != self.game_phase:
            self.game_phase = result
            self.event_handler.fire('gamePhaseChanged', result)
        return self.game_phase

    def is_impostor(self):
        # The character must stay immobile when it is reading the name
        if self._is_impostor is None:
            self._is_impostor = check_red(*PixelRegions.CHARACTER_NAME.value)
        return self._is_impostor

    def is_btn_use_active(self):
        result = check_pixel_color(PixelPositions.MAIN_BTN.value, Colors.USE_BTN_ACTIVE.value)
        result = result or check_pixel_color(PixelPositions.MAIN_BTN.value, Colors.USE_BTN_ACTIVE_RED.value)
        if result != self.is_btn_use_active:
            self._is_btn_use_active = result
            self.event_handler.fire('btnUseChanged', result)
        return result

    def is_btn_report_active(self):
        result = check_red(*PixelRegions.REPORT_BTN.value)
        if result != self._is_btn_report_active:
            self._is_btn_report_active = result
            self.event_handler.fire('btnReportChanged', result)
        return result

    def is_btn_kill_active(self):
        result = check_red(*PixelRegions.KILL_BTN.value)
        if result != self._is_btn_kill_active:
            self._is_btn_kill_active = result
            self.event_handler.fire('btnKillChanged', result)
        return result

    def is_btn_vent_active(self):
        result = check_pixel_color(PixelPositions.MAIN_BTN.value, Colors.VENT_BTN_ACTIVE.value)
        if result != self.is_btn_vent_active:
            self._is_btn_vent_active = result
            self.event_handler.fire('btnVentChanged', result)
        return result

    def is_btn_sabotage_active(self):
        result = check_pixel_color(PixelPositions.MAIN_BTN.value, Colors.SABOTAGE_BTN_ACTIVE.value)
        if result != self.is_btn_sabotage_active:
            self._is_btn_sabotage_active = result
            self.event_handler.fire('btnSabotageChanged', result)
        return result

    def is_btn_admin_active(self):
        result = check_pixel_color(PixelPositions.MAIN_BTN.value, Colors.ADMIN_BTN_ACTIVE.value)
        if result != self.is_btn_admin_active:
            self._is_btn_admin_active = result
            self.event_handler.fire('btnAdminChanged', result)
        return result

    def is_btn_security_active(self):
        result = check_pixel_color(PixelPositions.MAIN_BTN.value, Colors.SECURITY_BTN_ACTIVE.value)
        if result != self.is_btn_security_active:
            self._is_btn_security_active = result
            self.event_handler.fire('btnSecurityChanged', result)
        return result

    def is_sabotage_running(self, tasks_text=None):
        if tasks_text is None:
            tasks_text = self.tasks_text

        sabotage_running = None
        for task_text in TasksTexts.get_sabotage_texts():
            if is_in_text(task_text.value, tasks_text):
                sabotage_running = task_text
                break

        is_sabotage_running = sabotage_running is not None
        if is_sabotage_running != self._is_sabotage_running:
            self.sabotage_running = TaskType.get_sabotage_from_text(sabotage_running) if is_sabotage_running else None
            self._is_sabotage_running = is_sabotage_running
            self.event_handler.fire('sabotageRunningChanged', self.sabotage_running)
        return self._is_sabotage_running
