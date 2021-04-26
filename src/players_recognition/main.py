import os
import cv2.cv2 as cv
import numpy as np
import os
from time import time, sleep
import pyautogui
from matplotlib import pyplot as plt

from window_capture import WindowCapture
from vision import Vision

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def run():
    # load the trained model
    cascade_model = cv.CascadeClassifier('cascade_model/cascade.xml')
    # load an empty Vision class
    vision = Vision(None)

    # sleep(3)

    loop_time = time()
    while(True):

        # get an updated image of the game
        screenshot = np.array(pyautogui.screenshot())

        # do object detection
        rectangles = cascade_model.detectMultiScale(screenshot)

        # draw the detection results onto the original image
        detection_image = vision.draw_rectangles(screenshot, rectangles)

        # display the images
        # cv.startWindowThread()
        # cv.namedWindow('Matches')
        cv.imshow('Matches', detection_image)
        cv.waitKey(1)
        # plt.imshow(detection_image)
        # plt.show()

        # debug the loop rate
        print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()

    print('Done.')

if __name__ == '__main__':
    run()