import os

import cv2 as cv
import numpy as np
import os
from time import time
from window_capture import WindowCapture
from vision import Vision


def run():
    # Change the working directory to the folder this script is in.
    # Doing this because I'll be putting the files from each video in their own folder on GitHub
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


    # initialize the WindowCapture class
    wincap = WindowCapture('Among Us')

    # load the trained model
    # cascade_limestone = cv.CascadeClassifier('limestone_model_final.xml')
    # load an empty Vision class
    vision_limestone = Vision(None)

    loop_time = time()
    while(True):

        # get an updated image of the game
        screenshot = wincap.get_screenshot()

        # do object detection
        # rectangles = cascade_limestone.detectMultiScale(screenshot)

        # draw the detection results onto the original image
        # detection_image = vision_limestone.draw_rectangles(screenshot, rectangles)

        # display the images
        # cv.imshow('Matches', detection_image)

        # debug the loop rate
        print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()

        # press 'q' with the output window focused to exit.
        # press 'f' to save screenshot as a positive image, press 'd' to 
        # save as a negative image.
        # waits 1 ms every loop to process key presses
        key = cv.waitKey()
        print(key)
        if key == ord('q'):
            cv.destroyAllWindows()
            break
        elif key == ord('f'):
            cv.imwrite('positive/{}.jpg'.format(loop_time), screenshot)
        elif key == ord('d'):
            cv.imwrite('negative/{}.jpg'.format(loop_time), screenshot)

    print('Done.')

# reads all the files in the /negative folder and generates neg.txt from them.
# we'll run it manually like this:
# $ python
# Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:21:23) [MSC v.1916 32 bit (Intel)] on win32
# Type "help", "copyright", "credits" or "license" for more information.
# >>> from cascadeutils import generate_negative_description_file
# >>> generate_negative_description_file()
# >>> exit()
def generate_negative_description_file():
    # open the output file for writing. will overwrite all existing data in there
    with open('neg.txt', 'w') as f:
        # loop over all the filenames
        for filename in os.listdir('negative'):
            f.write('negative/' + filename + '\n')

# the opencv_annotation executable can be found in opencv/build/x64/vc15/bin
# generate positive description file using:
# $ C:/Users/Ben/learncodebygaming/opencv/build/x64/vc15/bin/opencv_annotation.exe --annotations=pos.txt --images=positive/

# You click once to set the upper left corner, then again to set the lower right corner.
# Press 'c' to confirm.
# Or 'd' to undo the previous confirmation.
# When done, click 'n' to move to the next image.
# Press 'esc' to exit.
# Will exit automatically when you've annotated all of the images

# generate positive samples from the annotations to get a vector file using:
# $ C:/Users/Ben/learncodebygaming/opencv/build/x64/vc15/bin/opencv_createsamples.exe -info pos.txt -w 24 -h 24 -num 1000 -vec pos.vec

# train the cascade classifier model using:
# $ C:/Users/Ben/learncodebygaming/opencv/build/x64/vc15/bin/opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -numPos 200 -numNeg 100 -numStages 10 -w 24 -h 24

# my final classifier training arguments:
# $ C:/Users/Ben/learncodebygaming/opencv/build/x64/vc15/bin/opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -precalcValBufSize 6000 -precalcIdxBufSize 6000 -numPos 200 -numNeg 1000 -numStages 12 -w 24 -h 24 -maxFalseAlarmRate 0.4 -minHitRate 0.999
