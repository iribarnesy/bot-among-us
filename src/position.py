import pyautogui
import time

class Directions:
    UP = "up"
    RIGHT_UP = "right-up"
    RIGHT = "right"
    RIGHT_DOWN = "right-down"
    DOWN = "down"
    LEFT_DOWN = "left-down"
    LEFT = "left"
    LEFT_UP = "left-up"

class Position:
    def __init__(self):
        self.vertical_position = 0
        self.horizontal_position = 0
        # speed = number of pixels by seconds when we press a key, on a 1920 * 1080 screen.
        self.speed_straight = 102
        self.speed_diagonal = 72

    def find_me(self):
        # Display the map
        pyautogui.press('tab')
        time.sleep(0.1)
        # find the character
        coordinates = pyautogui.locateOnScreen('./src/img/map_character.png', grayscale=True, confidence=.65)
        center = pyautogui.center(coordinates)
        self.vertical_position = center.y
        self.horizontal_position = center.x
        # Close the map
        pyautogui.press('tab')

    def update_pos(self, distance_pix, direction):
        if direction == "up":
            self.vertical_position -= distance_pix
        elif direction == "down":
            self.vertical_position += distance_pix
        elif direction == "left":
            self.horizontal_position -= distance_pix
        else:
            self.horizontal_position += distance_pix

    def move_straight(self, distance_pix, direction):
        # Compute the time to travel at the speed.
        time_wait = distance_pix/self.speed_straight
        # Move
        pyautogui.keyDown(direction)
        time.sleep(time_wait)
        pyautogui.keyUp(direction)
    
    def move_diagonal(self, distance_pix, direction1, direction2):
        # Compute the time to travel at the speed.
        time_wait = distance_pix/self.speed_diagonal
        # Move
        pyautogui.keyDown(direction1)
        pyautogui.keyDown(direction2)
        time.sleep(time_wait)
        pyautogui.keyUp(direction1)
        pyautogui.keyUp(direction2)
    
    def move(self,distance_pix,direction):
        pyautogui.PAUSE = 0
        directions = direction.split("-")
        if len(directions) == 1:
            # move
            self.move_straight(distance_pix, direction)
            # Update position
            self.update_pos(distance_pix, direction)
        else:
            # move
            self.move_diagonal(distance_pix,directions[0],directions[1])
            # Update position
            self.update_pos(distance_pix, directions[0])
            self.update_pos(distance_pix, directions[1])