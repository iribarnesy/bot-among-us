from enum import Enum

class Colors(Enum):
    # Main button (1769, 942)
    USE_BTN_ACTIVE = (170, 187, 187)
    USE_BTN_ACTIVE_RED = (202, 117, 117)
    USE_BTN_INACTIVE = (94, 108, 108)
    SECURITY_BTN_ACTIVE = (0, 205, 104)
    ADMIN_BTN_ACTIVE = (85, 102, 102)
    SABOTAGE_BTN_ACTIVE = (255, 0, 0)
    VENT_BTN_ACTIVE = (192, 199, 199)
    CUSTOMIZE_BTN_ACTIVE = (238, 238, 238)

    RED_TEXT = (255, 0, 0)
    YELLOW_TEXT = (245, 229, 4)
    WHITE_TEXT = (255, 255, 255)

    RED_PLAYER = ((198, 17, 17),(108, 15, 15))
    BLUE_PLAYER = ((19, 46, 210),(16, 30, 114))
    GREEN_PLAYER = ((17, 128, 45),(15, 72, 30))
    YELLOW_PLAYER = ((246, 246, 87),(132, 132, 51))
    ORANGE_PLAYER = ((240, 125, 13),(129, 71, 13))
    PINK_PLAYER = ((238, 84, 187),(128, 50, 102))
    PURPLE_PLAYER = ((107, 47, 188),(61, 31, 103))
    WHITE_PLAYER = ((215, 225, 241),(116, 122, 130))
    BLACK_PLAYER = ((63, 71, 78),(39 , 43 , 47))
    BROWN_PLAYER = ((113, 73, 30),(64, 44, 22 )) 
    CYAN_PLAYER = ((56, 255, 221),(35, 137, 120))
    LIME_PLAYER = ((80, 240, 57),(48, 129, 36))

    RED_PLAYER_VOTE = (190, 63, 70)
    BLUE_PLAYER_VOTE = (61, 88, 215)
    GREEN_PLAYER_VOTE = (60, 149, 93)
    YELLOW_PLAYER_VOTE = (226, 234, 123)
    ORANGE_PLAYER_VOTE = (226, 147, 69)
    PINK_PLAYER_VOTE = (221, 114, 197)
    PURPLE_PLAYER_VOTE = ((107, 47, 188),(59, 23, 124)) #
    WHITE_PLAYER_VOTE = ((215, 225, 241),(132, 149, 192)) #
    BLACK_PLAYER_VOTE = ((63, 71, 78),(30, 31, 38)) #
    BROWN_PLAYER_VOTE = ((113, 73, 30),(94, 38, 21))  #
    CYAN_PLAYER_VOTE = (89, 242, 224)
    LIME_PLAYER_VOTE = ((80, 240, 57),(21, 168, 66))  #

    @classmethod
    def get_text_colors(cls):
        return [cls.RED_TEXT.value, cls.YELLOW_TEXT.value, cls.WHITE_TEXT.value]
    
    @classmethod
    def get_all_player_colors(cls):
        return [cls.RED_PLAYER.value, cls.BLUE_PLAYER.value, cls.GREEN_PLAYER.value, cls.YELLOW_PLAYER.value,
                cls.ORANGE_PLAYER.value, cls.PINK_PLAYER.value, cls.PURPLE_PLAYER.value, cls.WHITE_PLAYER.value,
                cls.BLACK_PLAYER.value, cls.BROWN_PLAYER.value, cls.CYAN_PLAYER.value, cls.LIME_PLAYER.value]

class PixelPositions(Enum):
    MAIN_BTN = (1769, 942)
    OPEN_TASKS_BTN = (0, 290)
    CLOSE_TASKS_BTN = (70, 290)

class PixelRegions(Enum):
    REPORT_BTN = (1670,630),(1870,830)
    KILL_BTN = (1480,890),(1640,1050)
    CHARACTER_NAME = (850,350),(1020,480)
    TASKS_TAB = (18,120),(748,1080)