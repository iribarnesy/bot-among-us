import pyautogui
from threading import Lock, Thread
from PIL import ImageGrab
from typing import Tuple
import time
import sys
import trace

from src.enums.pixels import PixelPositions

def open_tasks_tab():
    pyautogui.moveTo(PixelPositions.OPEN_TASKS_BTN.value)
    pyautogui.click()
    time.sleep(0.1)

def close_tasks_tab():
    pyautogui.moveTo(PixelPositions.CLOSE_TASKS_BTN.value)
    pyautogui.click()
    time.sleep(0.1)

def flatten(region: Tuple):
      top_left, bottom_right = region
      x1, y1 = top_left
      x2, y2 = bottom_right
      return x1, y1, x2, y2

# def detect_text(path):
#     """Detects text in the file."""
#     from google.cloud import vision
#     import io
#     client = vision.ImageAnnotatorClient()

#     with io.open(path, 'rb') as image_file:
#         content = image_file.read()

#     image = vision.Image(content=content)

#     response = client.text_detection(image=image)
#     texts = response.text_annotations
#     print('Texts:')

#     for text in texts:
#         print('\n"{}"'.format(text.description))

#         vertices = (['({},{})'.format(vertex.x, vertex.y)
#                     for vertex in text.bounding_poly.vertices])

#         print('bounds: {}'.format(','.join(vertices)))

#     if response.error.message:
#         raise Exception(
#             '{}\nFor more info on error messages, check: '
#             'https://cloud.google.com/apis/design/errors'.format(
#                 response.error.message))

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