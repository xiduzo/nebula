import cv2
import time
import random
# import RPi.GPIO as GPIO

videoSource = 'src/videos/Finalcom_Infrapurple.mov' # set initial video source
cap = cv2.VideoCapture(videoSource)
playingVideo = True

FPS = 24.0 # mostly use 24 i guess
currentFrame = 0 # remember which frame we are at
videoFilter = ''; # dont apply any filter in the beginning?

# Raspberry pi setup
# GPIO.setup(17, GPIO.IN)
# GPIO.setup(18, GPIO.IN)
# GPIO.setup(19, GPIO.IN)
# GPIO.setup(20, GPIO.IN)

def rageQuit():
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
        # if GPIO.input(17):
        #     videoFilter = 'radio'
        # if GPIO.input(18):
        #     videoFilter = 'ultraviolet'
        # if GPIO.input(19):
        #     videoFilter = 'xray'
        # if GPIO.input(20):
        #     videoFilter = 'gamma'

        # For testing colors
        # if currentFrame % FPS == 0:
        #     filters = ['', 'radio', 'infrared', 'ultraviolet', 'xray', 'gamma']
        #     videoFilter = random.choice(filters)

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

            cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
            cv2.imshow('window',frame)
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
