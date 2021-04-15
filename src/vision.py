from enum import Enum

from src.enums.pixels import Colors, PixelPositions, PixelRegions
from src.utils import check_image, check_color, check_red, check_pixel_color

class GamePhase(Enum):
    Game = "game"
    Vote = "vote"
    Lobby = "lobby"

class VisionManager:
    SECONDS_BETWEEN_EACH_SCREEN = 3

    def __init__(self):
        self.vision_screen = None
        self.game_phase: GamePhase = None
        self._is_impostor = None
        # self.is_sabotage_running = None

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
