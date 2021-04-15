from enum import Enum

class Colors(Enum):
    # Main button (1769, 942)
    USE_BTN_ACTIVE = (170, 187, 187)
    USE_BTN_INACTIVE = (94, 108, 108)
    SECURITY_BTN_ACTIVE = (0, 205, 104)
    ADMIN_BTN_ACTIVE = (85, 102, 102)
    SABOTAGE_BTN_ACTIVE = (255, 0, 0)
    VENT_BTN_ACTIVE = (192, 199, 199)
    CUSTOMIZE_BTN_ACTIVE = (238, 238, 238)

class PixelPositions(Enum):
    MAIN_BTN = (1769, 942)

class PixelRegions(Enum):
    REPORT_BTN = (1670,630),(1870,830)
    KILL_BTN = (1440,850),(1640,1050)
    CHARACTER_NAME = (900,420),(1020,480)