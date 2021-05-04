import pyautogui
import cv2.cv2 as cv
from threading import Lock, Thread
from PIL import ImageGrab
from typing import Tuple
import time
import sys
import trace

from src.enums.pixels import PixelPositions

def draw_boxes(boxes, screenshot):
  line_color = (0, 255, 0)
  line_type = cv.LINE_4
  thickness = 5
  screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)
  for (ymin, xmin, ymax, xmax) in boxes:
      # determine the box positions
      top_left = (int(xmin * 1920), int(ymin * 1080))
      bottom_right = (int(xmax * 1920), int(ymax * 1080))
      # draw the box
      cv.rectangle(screenshot, top_left, bottom_right, line_color, thickness, line_type)
  return screenshot

def manhattan_distance(source, target):
    distance = abs(source[0]-target[0]) + abs(source[1]-target[1])
    return distance

def zero_pause_pyautogui_decorator(func):
    def wrapper():
        pyautogui.PAUSE = 0
        func()
        pyautogui.PAUSE = 0.1
    return wrapper

def open_tasks_tab():
    mouse_pos = pyautogui.position()
    pyautogui.moveTo(PixelPositions.OPEN_TASKS_BTN.value, _pause=0)
    pyautogui.click(_pause=0.001)
    pyautogui.moveTo(*mouse_pos, _pause=0)
    time.sleep(0.3)

def close_tasks_tab():
    mouse_pos = pyautogui.position()
    pyautogui.moveTo(PixelPositions.CLOSE_TASKS_BTN.value, _pause=0)
    pyautogui.click(_pause=0.001)
    pyautogui.moveTo(*mouse_pos, _pause=0)
    time.sleep(0.1)

def flatten(region: Tuple):
      top_left, bottom_right = region
      x1, y1 = top_left
      x2, y2 = bottom_right
      return x1, y1, x2, y2

def is_in_text(short_text_to_find, long_text):
      """ For now, find exactly the string.
      TODO: find when the string is almost matching. For example :
        'Sbotged' should be found in 'Comms Sabotaged'
      """
      res = long_text.find(short_text_to_find)
      return res != -1
            
      
def check_color(top_left_corner, bottom_right_corner, color):
    # TODO: fix because it's doesn't work, it is fitted to red only
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

def check_pixel_color(pixel_position, color):
    x, y = pixel_position
    im = pyautogui.screenshot(region=(x, y, 1, 1))
    return im.getpixel((0,0)) == color

def check_image(image_path, grayscale=True, confidence=.65):
    coordinates = pyautogui.locateOnScreen(image_path, grayscale=grayscale, confidence=confidence)
    return coordinates is not None


def check_red(top_left_corner, bottom_right_corner):
    red = (220, 30, 30)
    return check_color(top_left_corner, bottom_right_corner, red)


class KillableThread(Thread):
  def __init__(self, *args, **keywords):
    Thread.__init__(self, *args, **keywords)
    self.killed = False
  
  def start(self):
    self.__run_backup = self.run
    self.run = self.__run      
    Thread.start(self)
  
  def __run(self):
    sys.settrace(self.globaltrace)
    self.__run_backup()
    self.run = self.__run_backup
  
  def globaltrace(self, frame, event, arg):
    if event == 'call':
      return self.localtrace
    else:
      return None
  
  def localtrace(self, frame, event, arg):
    if self.killed:
      if event == 'line':
        raise SystemExit()
    return self.localtrace
  
  def kill(self):
    self.killed = True

class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    Source: https://refactoring.guru/fr/design-patterns/singleton/python/example#example-0
    """

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

def FOCUS_AMONG_SCREEN():
    among_window = pyautogui.getWindowsWithTitle("Among Us")[0]
    if not among_window.isActive:
        if among_window.isMaximized:
            among_window.minimize()
        among_window.maximize()
        pyautogui.click(among_window.center)