from PIL import ImageGrab

class VisionManager:
    SECONDS_DURING_EACH_SCREEN = 3

    def __init__(self):
        self.vision_screen = None
        self.game_phase = None
        self.is_impostor = None
        self.is_sabotage_active = None

        self.is_map_active = None
        self.is_btn_use_active = None
        self.is_btn_admin_active = None
        self.is_btn_security_active = None
        self.is_btn_report_active = None
        self.is_btn_sabotage_active = None
        self.is_btn_kill_active = None
        self.is_btn_vent_active = None
        
    def check_color(self, top_left_corner, bottom_right_corner, color):
        x1, y1 = top_left_corner
        x2, y2 = bottom_right_corner
        red, green, blue = color
        
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        pix = img.load()
        
        for pix_x in range(img.size[0]):
            for pix_y in range(img.size[1]):
                r, g, b = pix[(pix_x, pix_y)]
                if r > red and g < green and b < blue:
                    return True
        return False

    def check_red(self, top_left_corner, bottom_right_corner):
        red = (220, 30, 30)
        return self.check_color(top_left_corner, bottom_right_corner, red)

    def checkImposteur(self):
        self.is_impostor = self.check_red((900,420),(1020,480))
        return self.is_impostor

    def checkReport(self):
        self.is_btn_report_active = self.check_red((1670,630),(1870,830))
        return self.is_btn_report_active
    
    def checkKill(self):
        self.is_btn_kill_active = self.check_red((1440,850),(1640,1050))
        return self.is_btn_kill_active
