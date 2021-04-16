from enum import Enum
import time
import pyautogui
from eventhandler import EventHandler

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
        self._is_btn_use_active = None
        self._is_btn_report_active = None
        self._is_btn_kill_active = None
        self._is_btn_vent_active = None
        self._is_btn_sabotage_active = None
        self._is_btn_admin_active = None
        self._is_btn_security_active = None
        # self.is_sabotage_running = None
        self.SECONDS_BETWEEN_EACH_SCREEN = 1
        self.MAX_ITERATIONS_FOR_THREAD = 10
        self.event_handler = EventHandler('gamePhaseChanged', 'btnUseChanged', 'btnReportChanged', 'btnKillChanged',
                                         'btnVentChanged', 'btnSabotageChanged', 'btnAdminChanged', 'btnSecurityChanged')


    def start_vision_loop(self):
        self.vision_thread = KillableThread(name="compute_screen", target=self.compute_screen)
        self.vision_thread.start()

    def compute_screen(self):
        for _ in range(self.MAX_ITERATIONS_FOR_THREAD):
            self.vision_screen = pyautogui.screenshot()
            self.is_btn_report_active()
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
            result = GamePhase.Vote   
        else:
            result = GamePhase.Game

        if result != self.game_phase:
            self.event_handler.fire('gamePhaseChanged', result)
            self.game_phase = result
        return self.game_phase

    def is_impostor(self):
        if self._is_impostor is None:
            self._is_impostor = check_red(*PixelRegions.CHARACTER_NAME.value)
        return self._is_impostor

    def is_btn_use_active(self):
        result = check_pixel_color(PixelPositions.MAIN_BTN.value, Colors.USE_BTN_ACTIVE.value)
        if result != self.is_btn_use_active:
            self.event_handler.fire('btnUseChanged', result)
            self._is_btn_use_active = result
        return result

    def is_btn_report_active(self):
        result = check_red(*PixelRegions.REPORT_BTN.value)
        if result != self._is_btn_report_active:
            self.event_handler.fire('btnReportChanged', result)
            self.__is_btn_report_active = result
        return result

    def is_btn_kill_active(self):
        result = check_red(*PixelRegions.KILL_BTN.value)
        if result != self.is_btn_kill_active:
            self.event_handler.fire('btnKillChanged', result)
            self._is_btn_kill_active = result
        return result

    def is_btn_vent_active(self):
        result = check_pixel_color(PixelPositions.MAIN_BTN.value, Colors.VENT_BTN_ACTIVE.value)
        if result != self.is_btn_vent_active:
            self.event_handler.fire('btnVentChanged', result)
            self._is_btn_vent_active = result
        return result

    def is_btn_sabotage_active(self):
        result = check_pixel_color(PixelPositions.MAIN_BTN.value, Colors.SABOTAGE_BTN_ACTIVE.value)
        if result != self.is_btn_sabotage_active:
            self.event_handler.fire('btnSabotageChanged', result)
            self._is_btn_sabotage_active = result
        return result

    def is_btn_admin_active(self):
        result = check_pixel_color(PixelPositions.MAIN_BTN.value, Colors.ADMIN_BTN_ACTIVE.value)
        if result != self.is_btn_admin_active:
            self.event_handler.fire('btnAdminChanged', result)
            self._is_btn_admin_active = result
        return result

    def is_btn_security_active(self):
        result = check_pixel_color(PixelPositions.MAIN_BTN.value, Colors.SECURITY_BTN_ACTIVE.value)
        if result != self.is_btn_security_active:
            self.event_handler.fire('btnSecurityChanged', result)
            self._is_btn_security_active = result
        return result
