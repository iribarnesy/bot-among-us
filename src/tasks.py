import pyautogui
import time
import numpy as np
import cv2
from PIL import ImageGrab, Image
import pytesseract
import math
from enum import Enum

import src.utils as utils

""" TaskManager
Presuppose that the task is opened in game, then solve the task.
This TaskManager contains the methodsto solve the main tasks.
Please create a new class, inheriting or composing this TaskManager, which fills the tasks array with the tasks specific to the game map (cf. game_map.py)
"""
class TaskType(Enum):
    Troubleshoot = 0
    Swipe_Card = 1
    Download_Upload = 2
    Fuel_Engines = 3
    Divert_Power = 4
    Empty_Chute = 5
    Accept_Power = 6
    Fix_Wires = 7
    Prime_Shields = 8
    Inspect_Sample = 9
    Stabilize_Steering = 10
    Submit_Scan = 11
    Align_Engine_Output = 12
    Clear_Asteroids = 13
    Clean_O2_Filter = 14
    Calibrate_Distributor = 15
    Start_Reactor = 16
    Chart_Course = 17
    Unlock_Manifold = 18
    Sabotage_O2 = 19
    Sabotage_Com = 20
    Sabotage_Reactor = 21
    Sabotage_Elec = 22

class Task:
    def __init__(self, index, name, location, indicator_location=None, solve_function=None, task_type=None):
        self.index = index
        self.name = name
        self.location = location
        self.indicator_location = indicator_location
        self.solve_function = solve_function
        self.task_type = task_type

    def solve(self):
        return self.solve_function()
    
    def __repr__(self):
        return f"{self.index}: {self.name}"

class TaskManager(metaclass=utils.SingletonMeta):
    MAIN_BUTTON_LOCATION = (1800, 930)

    def __init__(self):
        self.tasks = []
        self.sabotage = []

    def __repr__(self):
        tasks = "\n".join(str(t) for t in self.tasks)
        return tasks

    def start_task(self):
        pyautogui.moveTo(self.MAIN_BUTTON_LOCATION)
        pyautogui.click()
        time.sleep(1)

    def swipe_card(self):
        pyautogui.moveTo(777, 814)
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(540, 400)
        pyautogui.drag(900, 0, 1.1, button='left')

    def download_upload(self):
        pyautogui.moveTo(970, 650)
        pyautogui.click()

    def accept_power(self):
        pyautogui.moveTo(956, 539)
        pyautogui.click()

    def fuel_engines(self):
        pyautogui.moveTo(1470, 880)
        pyautogui.mouseDown()
        time.sleep(5)
        pyautogui.mouseUp()

    def submit_scan(self):
        time.sleep(10)

    def divert_power(self):
        sliders = [(620, 780), (715, 780), (813, 780), (912, 780), (1007, 780), (1101, 780), (1201, 780), (1297, 780)]
        img = ImageGrab.grab(bbox=(0,0 ,1920,1080))
        pix = img.load()
        for i in sliders:
            if pix[i][0] > 50:
                pyautogui.moveTo(i)
                pyautogui.drag(0, -100, 0.5, button='left')
                break

    def empty_chute(self):
        pyautogui.moveTo(1270,420)
        pyautogui.mouseDown()
        pyautogui.moveTo(1270,720,0.2)
        time.sleep(3)
        pyautogui.mouseUp()

    def fix_wires(self):
        wires = [(560, 270), (560, 460), (560, 650), (560, 830), (1330, 270), (1330, 460), (1330, 650), (1330, 830)]
        img = ImageGrab.grab(bbox=(0,0 ,1920,1080))
        pix = img.load()

        for i in range(0, 4):
            for j in range(4, 8):
                if pix[wires[i]] == pix[wires[j]]:
                    pyautogui.moveTo(wires[i])
                    pyautogui.mouseDown()
                    time.sleep(0.01)
                    pyautogui.moveTo(wires[j])
                    pyautogui.mouseUp()

    def prime_shields(self):
        tiles = [(1050, 210), (1261, 330), (1261, 586), (964, 909), (635, 725), (635, 454), (964, 425)]
        img = ImageGrab.grab(bbox=(0,0 ,1920,1080))
        pix = img.load()
        for tile in tiles:
            r, g, b = pix[tile]
            if g < 200 and b < 200:
                pyautogui.moveTo(tile)
                pyautogui.click()
                

    def inspect_sample(self):
        tubes = [(732, 590), (850, 590), (960, 590), (1075, 590), (1190, 590)]
        red = (246, 134, 134)
        pyautogui.moveTo(1260, 930)
        pyautogui.click()
        time.sleep(70)
        img = ImageGrab.grab(bbox=(0,0 ,1920,1080))
        pix = img.load()
        for tube in tubes:
            if pix[tube] == red:
                pyautogui.moveTo(tube[0], 850)
                pyautogui.click()

    def align_engine_output(self):
        img = ImageGrab.grab(bbox=(0,0 ,1920,1080))
        im = np.array(img)
        marker = (202, 202, 216)
        Y,X = np.where(np.all(im==marker, axis=2))
        pyautogui.moveTo(X[0], Y[0])
        pyautogui.mouseDown()
        pyautogui.moveTo(1250, 540)
        pyautogui.mouseUp()

    def clear_asteroids(self): # Méthode bourrine - spam
        pyautogui.PAUSE = 0
        y_min = 250
        y_max = 850
        x_val = 1260
        pos_y = y_min
        padding = 60

        refresh_img = 0
        freq_refresh = 50

        white_croix = (238, 238, 238)

        img = ImageGrab.grab(bbox=(479,130 ,480,131))
        pix = img.load()

        while pix[0,0] == white_croix:
            pos_y = pos_y + padding
            if pos_y > y_max:
                pos_y = y_min

            pyautogui.moveTo(x_val, pos_y)
            pyautogui.click()

            if refresh_img % freq_refresh == 0:
                img = ImageGrab.grab(bbox=(479,130 ,480,131))
                pix = img.load()
                refresh_img = 0
            else:
                refresh_img = refresh_img + 1

    def clean_O2_filter(self):
        while True:
            img = ImageGrab.grab(bbox=(0,0 ,1920,1080))
            array = np.array(img)
            leaf = (198, 150, 66)
            Y,X = np.where(np.all(array==leaf, axis=2))
            if len(X) != 0:
                pyautogui.moveTo(X[0], Y[0])
                pyautogui.dragTo(668, 555, 0.5, button='left')
            else:
                break

    def calibrate_distributor(self):
        distributor = [(800, 300), (800, 550), (800, 830)]
        buttons = [(1230, 310), (1230, 580), (1230, 840)]
        on = (71, 73, 71)
        for i in range(3):
            pyautogui.moveTo(buttons[i])
            while True:
                img = ImageGrab.grab(bbox=(0,0 ,1920,1080))
                pix = img.load()
                if pix[distributor[i]] == on:
                    pyautogui.click()
                    break

    def start_reactor(self): 
        lights = [(500, 450), (650, 450), (790, 450), (500, 600), (650, 600), (790, 600), (500, 750), (650, 750), (790, 750)]
        buttons = [(1140, 450), (1260, 450), (1400, 450), (1140, 600), (1260, 600), (1400, 600), (1140, 750), (1260, 750), (1400, 750), ]
        
        on = (68, 168, 255)
        for i in range(0, 5):
            flashed = []
            while True:
                img = ImageGrab.grab(bbox=(0,0 ,1920,1080))
                pix = img.load()
                for j in range(9):
                    if(pix[lights[j]] == on):
                        flashed.append(j)
                        time.sleep(0.3)

                if len(flashed) == (i + 1):
                    break
                
            time.sleep(1)
            print(flashed)
            for k in flashed:
                pyautogui.moveTo(buttons[k])
                pyautogui.click()
                time.sleep(0.2)        

    def stabilize_steering(self):
        pyautogui.moveTo(960, 537)
        pyautogui.click()

    def chart_course(self):
        img = ImageGrab.grab(bbox=(465,265,1455,815))
        array = np.array(img)

        # special color
        colors = [ (37, 111, 160), (36, 112, 161), (135, 161, 176), (100, 60, 0), (255, 255, 255) ]
        nodes = [565, 760, 960, 1160, 1350]

        pix = img.load()
        Y,X = np.where(np.all(array==colors[0], axis=2))
        for node in nodes:
            x_avg = 0
            y_avg = 0
            counter = 0
            for i in range(len(X)):
                if ((X[i] > (node-40)-465) and (X[i] < (node+40)-465)):
                    print(str(X[i]) + ", " + str(Y[i]))
                    x_avg += X[i]
                    y_avg += Y[i]
                    counter += 1
            if(counter != 0):
                pyautogui.moveTo(x_avg/counter+500, y_avg/counter+265)
                pyautogui.mouseDown()
                

    def unlock_manifold_get_numbers(self):
        self.start_task()
        merged = Image.new("RGB", (1150, 115))
        number_box_start = [(585,395), (737, 395), (890, 395), (1040, 395), (1195, 395), (585,548), (737, 548), (890, 548), (1040, 548), (1195, 548)]
        
        for i in range(10):
            img = ImageGrab.grab(bbox=(number_box_start[i][0]+10,number_box_start[i][1]+10,number_box_start[i][0]+125,number_box_start[i][1]+125))
            merged.paste(img, (int(i * 115),0))
            
        img = np.array(merged)
        img = img[:, :, ::-1].copy()
        img[:,:,0] = np.zeros([img.shape[0], img.shape[1]])
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Connect text with a horizontal shaped kernel
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,3))
        dilate = cv2.dilate(thresh, kernel, iterations=3)

        # Remove non-text contours using aspect ratio filtering
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            aspect = w/h
            if aspect < 3:
                cv2.drawContours(thresh, [c], -1, (0,0,0), -1)

        # Invert image and OCR
        result = 255 - thresh
        result = cv2.GaussianBlur(result,(5,5),cv2.BORDER_DEFAULT)
        cv2.imwrite("merged.png", result)
        data = pytesseract.image_to_string(result, lang='eng',config='--psm 6 -c tessedit_char_whitelist=123456789N')
        return data.strip()

    def unlock_manifold(self):
        while True:
            data = self.unlock_manifold_get_numbers()
            whitelist = "123456789N"
            print(data)
            if(len(data) != 10):
                self.start_task()
                continue
            for i in data:
                for j in whitelist:
                    if i == j:
                        whitelist = whitelist.replace(j, "")
            if (whitelist == ""):
                self.input_numbers(data)
                break
            else:
                self.start_task()
                continue

    def input_numbers(self, data):
        numbers = [(660, 450), (820, 450), (960, 450), (1120, 450), (1260, 450), (660, 620), (820, 620), (960, 620), (1120, 620), (1260, 620)]
        order = list(data)
        for i in range(1, 11):
            for j in range(10):
                if order[j] == str(i) or (order[j] == "N" and i == 10):
                    pyautogui.moveTo(numbers[j])
                    pyautogui.click()
        time.sleep(10)

    def sabotage_oxygen(self):
        img = ImageGrab.grab(bbox=(0,0 ,1920,1080))
        img.save("C:/Users/Administrator/Desktop/bot-among-us/src/img/temp.png")

        img = cv2.imread("C:/Users/Administrator/Desktop/bot-among-us/src/img/temp.png")

        coord_numbers = [(959,864), (795,381), (957,374), (1118,369), (819,537), (934,535), (1113,526), (814,688), (972,729), (1144,851)]
        coord_validate = (1113,875)
        coord_code = np.array([[[1246,362]], [[1227,333]], [[1327,280]], [[1360,322]]])
        rect = cv2.minAreaRect(coord_code)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
        width = int(rect[1][0])
        height = int(rect[1][1])
        src_pts = box.astype("float32")
        dst_pts = np.array([[0, height-1],
                        [0, 0],
                        [width-1, 0],
                        [width-1, height-1]], dtype="float32")
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        warped = cv2.warpPerspective(img, M, (width, height))
        image = cv2.rotate(warped, cv2.cv2.ROTATE_90_CLOCKWISE)

        data = pytesseract.image_to_string(image, lang='eng',config='--psm 6 -c tessedit_char_whitelist=0123456789')
        for el in data[0:5]:
            val = int(el)
            if val >= 0 and val < 10:
                pyautogui.moveTo(coord_numbers[val])
                pyautogui.click()
        pyautogui.moveTo(coord_validate)
        pyautogui.click()
    
    def sabotage_communication(self):
        pyautogui.PAUSE = 0
        down_left_button = (1118, 879)
        mid_button = (1240, 685)
        # down_right_button = (1366, 880)
        circle_center = (1241, 820)
        circle_radius = 138
        start_angle = 2.6710101913802777
        end_angle = (2 * math.pi) + 0.4375391366820185
        # red_light = (1352, 667)
        # green_light = (1403, 670)

        # Move button to down left.

        pyautogui.moveTo(mid_button)
        pyautogui.dragTo(down_left_button[0], down_left_button[1], 0.3, button='left')
        pyautogui.mouseDown()

        white_cross = (238, 238, 238)
        img = ImageGrab.grab(bbox=(510,382 ,511,383))
        pix = img.load()

        # we pass over most of the circle (angle from 2.6 to 2 * pi)
        angle = start_angle
        refresh_img = 0
        freq_refresh = 10
        # fund_angle = 0 if never fund, 1 if found, 2 if founded before.
        fund_angle = 0
        start_fund_angle = start_angle
        end_fund_angle = end_angle

        while (pix[0,0] == white_cross) and (angle <= end_angle) and (fund_angle < 2):
            angle += 0.04
            pos_x = circle_center[0] + circle_radius * math.cos(angle)
            pos_y = circle_center[1] + circle_radius * math.sin(angle)
            pyautogui.moveTo(pos_x,pos_y)
            time.sleep(0.01)

            if refresh_img % freq_refresh == 0:
                img = ImageGrab.grab(bbox=(510,382 ,511,383))
                pix = img.load()
                imgTest = ImageGrab.grab(bbox=(1352,667 ,1353,668))
                pixTest = imgTest.load()
                # If the red light become switch off
                if(pixTest[0,0][0] < 255):
                    if fund_angle == 1 :
                        end_fund_angle = angle
                    elif fund_angle == 0 :
                        start_fund_angle = angle
                        end_fund_angle = angle
                        fund_angle = 1
                # If the red light switch on
                if (pixTest[0,0][0] == 255) and (fund_angle == 1):
                    fund_angle = 2

                refresh_img = 0
            else:
                refresh_img = refresh_img + 1
        
        pyautogui.mouseUp()
        time.sleep(0.5)

        # We fund the angle where the solution is. Now we go for it.

        pos_x_fake = circle_center[0] + circle_radius * math.cos(angle-0.5)
        pos_y_fake = circle_center[1] + circle_radius * math.sin(angle-0.5)

        pos_x_sol = circle_center[0] + circle_radius * math.cos(end_fund_angle)
        pos_y_sol = circle_center[1] + circle_radius * math.sin(end_fund_angle)
        pyautogui.dragTo(pos_x_fake, pos_y_fake, 0.3, button='left')
        time.sleep(0.5)
        pyautogui.dragTo(pos_x_sol, pos_y_sol, 0.3, button='left')


    def sabotage_reactor(self):
        pyautogui.moveTo(960, 720)
        pyautogui.mouseDown()

        img = ImageGrab.grab(bbox=(1299,199 ,1300,200))
        pix = img.load()

        while pix[0,0][0] > 250:
            time.sleep(0.1)
            img = ImageGrab.grab(bbox=(1299,199 ,1300,200))
            pix = img.load()

        pyautogui.mouseUp()

    def sabotage_electrical(self):
        coord_light = [(1, 10), (176,1), (347, 2), (521, 3), (697, 6)]
        right_green = (0, 255, 0)
        pos_x_img = 616
        pos_y_img = 895
        img = ImageGrab.grab(bbox=(pos_x_img ,pos_y_img ,1315 ,906))
        pix = img.load()
        while(pix[coord_light[0]] != right_green or pix[coord_light[1]] != right_green or pix[coord_light[2]] != right_green or pix[coord_light[3]] != right_green or pix[coord_light[4]] != right_green):
            for pt in coord_light:
                if pix[pt] != right_green:
                    pyautogui.moveTo(pos_x_img + pt[0], pos_y_img + pt[1] - 120)
                    pyautogui.click()
            img = ImageGrab.grab(bbox=(pos_x_img ,pos_y_img ,1315 ,906))
            pix = img.load()

    def troubleshoot(self):
        while True:
            time.sleep(1)
            print(pyautogui.position())

    def solve_task(self, option):
        if(option == TaskType.Troubleshoot):
            self.troubleshoot()
        elif(option == TaskType.Swipe_Card):
            self.start_task()
            self.swipe_card()
        elif(option == TaskType.Download_Upload):
            self.start_task()
            self.download_upload()
        elif(option == TaskType.Fuel_Engines):
            self.start_task()
            self.fuel_engines()
        elif(option == TaskType.Divert_Power):
            self.start_task()
            self.divert_power()
        elif(option == TaskType.Empty_Chute):
            self.start_task()
            self.empty_chute()
        elif(option == TaskType.Accept_Power):
            self.start_task()
            self.accept_power()
        elif(option == TaskType.Fix_Wires):
            self.start_task()
            self.fix_wires()
        elif(option == TaskType.Prime_Shields):
            self.start_task()
            self.prime_shields()
        elif(option == TaskType.Inspect_Sample):
            self.start_task()
            self.inspect_sample()
        elif(option == TaskType.Stabilize_Steering):
            self.start_task()
            self.stabilize_steering()
        elif(option == TaskType.Submit_Scan):
            self.start_task()
        elif(option == TaskType.Align_Engine_Output):
            self.start_task()
            self.align_engine_output()
        elif(option == TaskType.Clear_Asteroids):
            self.start_task()
            self.clear_asteroids()
        elif(option == TaskType.Clean_O2_Filter):
            self.start_task()
            self.clean_O2_filter()
        elif(option == TaskType.Calibrate_Distributor):
            self.start_task()
            self.calibrate_distributor()
        elif(option == TaskType.Start_Reactor):
            self.start_task()
            self.start_reactor()
        elif(option == TaskType.Chart_Course):
            self.start_task()
            self.chart_course()
        elif(option == TaskType.Unlock_Manifold):
            self.unlock_manifold()
        else:
            print("Invalid option, please try again!")
        
    def prompt_task(self):
        print("What task would you like to perform?:")
        print("\n".join([f"{getattr(TaskType, taskType)}: {taskType}" for taskType in vars(TaskType) if not taskType.startswith('__')]))
        return self.solve_task(int(input('options:')))
