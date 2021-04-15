from PIL import ImageGrab
import pyautogui
class VisionManager:
    SECONDS_BETWEEN_EACH_SCREEN = 3

    def __init__(self):
        self.vision_screen = None
        self.game_phase = None
        self.is_impostor = None
        # self.is_sabotage_active = None

        # self.is_map_active = None
        # self.is_btn_use_active = None
        # self.is_btn_admin_active = None
        # self.is_btn_security_active = None
        # self.is_btn_report_active = None
        # self.is_btn_sabotage_active = None
        # self.is_btn_kill_active = None
        # self.is_btn_vent_active = None


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


    def check_image(self, image_path):
        coordinates = pyautogui.locateOnScreen(image_path, grayscale=True, confidence=.65)
        
        if coordinates is None:
            return False
        else:
            return True


    def check_red(self, top_left_corner, bottom_right_corner):
        red = (220, 30, 30)
        return self.check_color(top_left_corner, bottom_right_corner, red)


    def is_btn_is_impostor_active(self):
        self.is_impostor = self.check_red((900,420),(1020,480))
        return self.is_impostor


    def is_btn_report_active(self):
        return self.check_red((1670,630),(1870,830))


    def is_btn_kill_active(self):
        return  self.check_red((1440,850),(1640,1050))

    def is_btn_vent_active(self):
        return self.check_image(r"src\img\vent_btn.png")


    def is_btn_sabotage_active(self):
        return self.check_image(r"src\img\sabotage_btn.png")


    def is_btn_admin_active(self):
        return self.check_image(r"src\img\admin_btn.PNG")
    
    def is_btn_security_active(self):
        return self.check_image(r"src\img\security_btn.PNG")