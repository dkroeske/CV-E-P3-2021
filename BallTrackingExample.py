# Playback video
import cv2
#import imutils
#import numpy as np
#import time

h_upper = 0
s_upper = 0
v_upper = 0
h_lower = 0
s_lower = 0
v_lower = 0

def on_h_upper(val):
    global h_upper
    h_upper = val

def on_s_upper(val):
    global s_upper
    s_upper = val

def on_v_upper(val):
    global v_upper
    v_upper = val

def on_h_lower(val):
    global h_lower
    h_lower = val

def on_s_lower(val):
    global s_lower
    s_lower = val

def on_v_lower(val):
    global v_lower
    v_lower = val

cv2.namedWindow("Trackbar")
cv2.createTrackbar('H upper', 'Trackbar', 0, 255, on_h_upper )
cv2.createTrackbar('S upper', 'Trackbar', 0, 255, on_s_upper )
cv2.createTrackbar('V upper', 'Trackbar', 0, 255, on_v_upper )
cv2.createTrackbar('H lower', 'Trackbar', 0, 255, on_h_lower )
cv2.createTrackbar('S lower', 'Trackbar', 0, 255, on_s_lower )
cv2.createTrackbar('V lower', 'Trackbar', 0, 255, on_v_lower )

while True:

    done = False
    capture = cv2.VideoCapture('resources/sample_video.mp4')
    if capture.isOpened() == False:
        print("Error opening video")

    while capture.isOpened():
        # Grap frame is possible
        ret, frame = capture.read()

        # Break als video af is gelopen
        if ret == True:

            # blur?
            blur = cv2.GaussianBlur(frame, (11,11), 0)

            # hsv
            hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

            # Selecteer op kleur optioneel mask, kun je vinden met de sliders
#            greenLower = (29, 86, 6)
#            greenUpper = (64, 255, 255)
#            mask = cv2.inRange(hsv, greenLower, greenUpper)
            mask = cv2.inRange(hsv, (h_lower, s_lower, v_lower), (h_upper, s_upper, v_upper))
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            # find contours
            contours_1, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for idx in range( len(contours_1)):
                color = (255, 255, 0)
                cv2.drawContours(frame, contours_1, idx, color, 1, cv2.LINE_8, hierarchy, 0)

            #
            contours_2 = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            for idx in range(len(contours_2)):
                (x,y), radius = cv2.minEnclosingCircle(contours_2[idx])
                cv2.circle( frame, (int(x), int(y)), int(radius), (0,0,255), 1)

            #c = max(contours_2, key=cv2.contourArea)
            #(x, y), radius = cv2.minEnclosingCircle(c)
            #cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 6)
            #print( '({},{})'.format( int(x), int(y) ) )

            cv2.imshow('Frame', frame)
            cv2.imshow('Blur', blur)
            cv2.imshow('HSV', hsv)
            cv2.imshow('Mask', mask)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                done = True
                break

        else:
            break

    if done:
        break


# Alles klaar. Release capture object
capture.release()
cv2.destroyAllWindows()
