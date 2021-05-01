import os
import cv2.cv2 as cv
import numpy as np
import os
from time import time, sleep
import pyautogui
from matplotlib import pyplot as plt

from vision import Vision
from players_detector import PlayersDetector, plot_prediction

def run():
    # load the trained model
    detection_model = PlayersDetector()

    loop_time = time()
    while(True):

        # get an updated image of the game
        screenshot = np.array(pyautogui.screenshot())

        # do object detection
        detections = detection_model.detect_from_np_array(screenshot)

        boxes = detections['detection_boxes'][0].numpy()
        scores = detections['detection_scores'][0].numpy()
        classes = detections['detection_classes'][0].numpy().astype(np.uint32)
        good_boxes = boxes[scores > 0.6]
        if len(good_boxes) > 1:
            print("Saw", len(good_boxes), "people")

        # draw the detection results onto the original image
        line_color = (0, 255, 0)
        line_type = cv.LINE_4
        for (ymin, xmin, ymax, xmax) in good_boxes:
            # determine the box positions
            top_left = (int(xmin * 1920), int(ymin * 1080))
            bottom_right = (int(xmax * 1920), int(ymax * 1080))
            # draw the box
            cv.rectangle(screenshot, top_left, bottom_right, line_color, thickness=5, lineType=line_type)
        screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)

        # display the images
        cv.namedWindow('Matches')
        cv.imshow('Matches', screenshot)
        cv.waitKey(1)

        # debug the loop rate
        print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()

    print('Done.')

if __name__ == '__main__':
    run()