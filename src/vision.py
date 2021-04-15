from enum import Enum
import time
import pyautogui

from src.enums.pixels import Colors, PixelPositions, PixelRegions
from src.utils import check_image, check_color, check_red, check_pixel_color
from src.utils import KillableThread, SingletonMeta

class GamePhase(Enum):
    Game = "game"
    Vote = "vote"
    Lobby = "lobby"

class VisionManager(metaclass=SingletonMeta):

    def __init__(self):
        self.vision_screen = None
        self.vision_thread = None
        self.game_phase: GamePhase = None
        self._is_impostor = None
        # self.is_sabotage_running = None
        self.SECONDS_BETWEEN_EACH_SCREEN = 1
        self.MAX_ITERATIONS_FOR_THREAD = 10


    def start_vision_loop(self):
        self.vision_thread = KillableThread(name="compute_screen", target=self.compute_screen)
        self.vision_thread.start()

    def compute_screen(self):
        for _ in range(self.MAX_ITERATIONS_FOR_THREAD):
            self.vision_screen = pyautogui.screenshot()
            time.sleep(self.SECONDS_BETWEEN_EACH_SCREEN)

    def is_vision_looping(self):
        if self.vision_thread is not None:
            return self.vision_thread.is_alive()
        else:
            return False

    def stop_vision_loop(self):
        self.vision_thread.kill()
        print("Terminate :", self.vision_thread)


    def get_game_phase(self):
        is_vote_phase = check_image(r"src\img\skip_vote.PNG")
        if is_vote_phase:
            self.game_phase = GamePhase.Vote
        else:
            self.game_phase = GamePhase.Game
        return self.game_phase

    def is_impostor(self):
        if self._is_impostor is None:
            self._is_impostor = check_red(*PixelRegions.CHARACTER_NAME.value)
        return self._is_impostor

    def is_btn_use_active(self):
        return check_pixel_color(PixelPositions.MAIN_BTN.value, Colors.USE_BTN_ACTIVE.value)

    def is_btn_report_active(self):
        return check_red(*PixelRegions.REPORT_BTN.value)

    def is_btn_kill_active(self):
        return check_red(*PixelRegions.KILL_BTN.value)

    def is_btn_vent_active(self):
        return check_pixel_color(PixelPositions.MAIN_BTN.value, Colors.VENT_BTN_ACTIVE.value)

    def is_btn_sabotage_active(self):
        return check_pixel_color(PixelPositions.MAIN_BTN.value, Colors.SABOTAGE_BTN_ACTIVE.value)

    def is_btn_admin_active(self):
        return check_pixel_color(PixelPositions.MAIN_BTN.value, Colors.ADMIN_BTN_ACTIVE.value)

    def is_btn_security_active(self):
        return check_pixel_color(PixelPositions.MAIN_BTN.value, Colors.SECURITY_BTN_ACTIVE.value)
