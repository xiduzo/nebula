import cv2
import time
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

videoSource = 'src/videos/centaur_1.mpg' # set initial video source
cap = cv2.VideoCapture(videoSource)
playingVideo = True

FPS = 24.0 # mostly use 24 i guess
currentFrame = 0 # remember which frame we are at
videoFilter = ''; # dont apply any filter in the beginning?

# Raspberry pi setup
NEBULA_FILTER_1 = 7
NEBULA_FILTER_2 = 11
NEBULA_FILTER_3 = 13
NEBULA_FILTER_4 = 15
GPIO.setup(NEBULA_FILTER_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(NEBULA_FILTER_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(NEBULA_FILTER_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(NEBULA_FILTER_4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

def rageQuit():
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()

def showVideo():
    global currentFrame
    global playingVideo
    global videoFilter

    cap.set(1, currentFrame)

    while playingVideo:
        ret, frame = cap.read()
        time.sleep(1.0 / FPS) # show video at playback rate
        
        # Switch filter according to the button press
        if (GPIO.input(NEBULA_FILTER_1) == False):
            videoFilter = 'gamma'
            GPIO.output(RED_1,0)
            GPIO.output(RED_2,1)
            GPIO.output(RED_3,1)
            GPIO.output(RED_4,1)
            GPIO.output(GREEN_1,1)
            GPIO.output(GREEN_2,0)
            GPIO.output(GREEN_3,0)
            GPIO.output(GREEN_4,0)
        if (GPIO.input(NEBULA_FILTER_2) == False):
            videoFilter = 'xray'
            GPIO.output(RED_1,1)
            GPIO.output(RED_2,0)
            GPIO.output(RED_3,1)
            GPIO.output(RED_4,1)
            GPIO.output(GREEN_1,0)
            GPIO.output(GREEN_2,1)
            GPIO.output(GREEN_3,0)
            GPIO.output(GREEN_4,0)
        if (GPIO.input(NEBULA_FILTER_3) == False):
            videoFilter = 'infrared'
            GPIO.output(RED_1,1)
            GPIO.output(RED_2,1)
            GPIO.output(RED_3,0)
            GPIO.output(RED_4,1)
            GPIO.output(GREEN_1,0)
            GPIO.output(GREEN_2,0)
            GPIO.output(GREEN_3,1)
            GPIO.output(GREEN_4,0)
        if (GPIO.input(NEBULA_FILTER_4) == False):
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
