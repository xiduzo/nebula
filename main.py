import cv2
import sys
import time
import random
import RPi.GPIO as GPIO

import Adafruit_MPR121.MPR121 as MPR121

GPIO.setmode(GPIO.BOARD)

videoSource = 'src/videos/centaur_1.mpg' # set initial video source
capVideo = cv2.VideoCapture(videoSource)
playingVideo = True

FPS = 24.0 # mostly use 24 i guess
currentFrame = 0 # remember which frame we are at
videoFilter = ''; # dont apply any filter in the beginning?

# capavative touch sensor
capTouch = MPR121.MPR121()

if not capTouch.begin():
    print('Error initializing MPR121.  Check your wiring!')
    sys.exit(1)

# Raspberry pi setup

# LED PINS
GREEN_1 = 40
RED_1 = 37
BLUE_1 = 38
GPIO.setup(RED_1,GPIO.OUT)
GPIO.setup(GREEN_1,GPIO.OUT)
GPIO.setup(BLUE_1,GPIO.OUT)
GREEN_2 = 31
RED_2 = 29
BLUE_2 = 32
GPIO.setup(RED_2,GPIO.OUT)
GPIO.setup(GREEN_2,GPIO.OUT)
GPIO.setup(BLUE_2,GPIO.OUT)
GREEN_3 = 36
RED_3 = 33
BLUE_3 = 35
GPIO.setup(RED_3,GPIO.OUT)
GPIO.setup(GREEN_3,GPIO.OUT)
GPIO.setup(BLUE_3,GPIO.OUT)
GREEN_4 = 22
RED_4 = 16
BLUE_4 = 18
GPIO.setup(RED_4,GPIO.OUT)
GPIO.setup(GREEN_4,GPIO.OUT)
GPIO.setup(BLUE_4,GPIO.OUT)

# We are not using the blue line
GPIO.output(BLUE_1,0)
GPIO.output(BLUE_2,0)
GPIO.output(BLUE_3,0)
GPIO.output(BLUE_4,0)

# Initial state
GPIO.output(GREEN_1,1)
GPIO.output(GREEN_2,0)
GPIO.output(GREEN_3,0)
GPIO.output(GREEN_4,0)
GPIO.output(RED_1,0)
GPIO.output(RED_2,0)
GPIO.output(RED_3,0)
GPIO.output(RED_4,0)

def turnOffLedLines(lines):
    for line in lines:
        GPIO.output(line, 0);

def rageQuit():
    GPIO.cleanup()
    capVideo.release()
    cv2.destroyAllWindows()

def showVideo():
    global currentFrame
    global playingVideo
    global videoFilter

    capVideo.set(0, currentFrame)

    while playingVideo:
        ret, frame = capVideo.read()
        time.sleep(1.0 / FPS) # show video at playback rate
        
        # Switch filter according to the button press
        if capTouch.is_touched(1):
            videoFilter = 'gamma'
            GPIO.output(RED_1,0)
            GPIO.output(RED_2,1)
            GPIO.output(RED_3,1)
            GPIO.output(RED_4,1)
            GPIO.output(GREEN_1,1)
            GPIO.output(GREEN_2,0)
            GPIO.output(GREEN_3,0)
            GPIO.output(GREEN_4,0)
        if capTouch.is_touched(2):
            videoFilter = 'xray'
            GPIO.output(RED_1,1)
            GPIO.output(RED_2,0)
            GPIO.output(RED_3,1)
            GPIO.output(RED_4,1)
            GPIO.output(GREEN_1,0)
            GPIO.output(GREEN_2,1)
            GPIO.output(GREEN_3,0)
            GPIO.output(GREEN_4,0)
        if capTouch.is_touched(3):
            videoFilter = 'infrared'
            GPIO.output(RED_1,1)
            GPIO.output(RED_2,1)
            GPIO.output(RED_3,0)
            GPIO.output(RED_4,1)
            GPIO.output(GREEN_1,0)
            GPIO.output(GREEN_2,0)
            GPIO.output(GREEN_3,1)
            GPIO.output(GREEN_4,0)
        if capTouch.is_touched(4):
            videoFilter = 'radio'
            GPIO.output(RED_1,1)
            GPIO.output(RED_2,1)
            GPIO.output(RED_3,1)
            GPIO.output(RED_4,0)
            GPIO.output(GREEN_1,0)
            GPIO.output(GREEN_2,0)
            GPIO.output(GREEN_3,0)
            GPIO.output(GREEN_4,1)

        # For testing colors
        # if currentFrame % FPS == 0:
        #    filters = ['', 'radio', 'infrared', 'ultraviolet', 'xray', 'gamma']
        #    videoFilter = random.choice(filters)

        if ret == True:
            currentFrame += 1

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Apply filter if nessecary
            if videoFilter == 'radio':
                frame = cv2.applyColorMap(gray_frame, cv2.COLORMAP_JET)
            elif videoFilter == 'infrared':
                frame = cv2.applyColorMap(gray_frame, cv2.COLORMAP_BONE)
            elif videoFilter == 'ultraviolet':
                frame = cv2.applyColorMap(gray_frame, cv2.COLORMAP_PINK)
            elif videoFilter == 'xray':
                frame = cv2.applyColorMap(gray_frame, cv2.COLORMAP_OCEAN)
            elif videoFilter == 'gamma':
                frame = cv2.applyColorMap(gray_frame, cv2.COLORMAP_HOT)

            #frame = cv2.resize(frame, (1280,1020))
            #cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
            #cv2.setWindowProperty("window",0,1)
            #cv2.namedWindow("test", cv2.WND_PROP_FULLSCREEN)          
            #cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
            cv2.imshow('test',frame)
            
        else:
            currentFrame = 0
            showVideo()

        # Press Q to stop everything
        if cv2.waitKey(1) & 0xFF == ord('q'):
            playingVideo = False
            rageQuit()
            break


def main():
    showVideo()

if __name__ == "__main__":
    main()
