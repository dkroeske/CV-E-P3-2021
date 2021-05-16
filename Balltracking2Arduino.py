# Playback video
import math

import cv2
import serial

# Connection to Arduino
arduino = serial.Serial(port='COM2', baudrate=115200, timeout=.1)

while True:

    done = False
    prevIsInHitRange = False
    nextIsInHitRange = False

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
            greenLower = (29, 86, 6)
            greenUpper = (64, 255, 255)
            mask = cv2.inRange(hsv, greenLower, greenUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            # find contours
            contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            for idx in range(len(contours)):
                (x,y), radius = cv2.minEnclosingCircle(contours[idx])
                cv2.circle( frame, (int(x), int(y)), int(radius), (0,0,255), 1)

            c = max(contours, key=cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(c)
            cv2.circle(frame, (int(x), int(y)), int(5), (0, 255, 0), -1)
            #print( '({},{})'.format( int(x), int(y) ) )

            # Check is (x,y) is in circle
            xc = 560
            yc = 770
            straal = 30
            dist = math.sqrt( math.pow(xc-x,2) + math.pow(yc-y,2))
            if dist < straal:
                cv2.circle(frame, (int(xc), int(yc)), int(straal), (0, 0, 255), -1)
            else:
                cv2.circle(frame, (int(xc), int(yc)), int(straal), (0, 0, 0), -1)

            # prev new
            #  f    f   -> hit = false
            #  f    t   -> hit = true
            #  t    f   -> hit = false
            #  t    t   -> hit = false

            if dist < straal - 5:
                nextIsInHitRange = True
            else:
                if dist < straal + 5:
                    nextIsInHitRange = False

            # Check if hit. Trigger Arduino
            if (prevIsInHitRange == False) and (nextIsInHitRange == True):
                cmd = "SHOOT:1".encode("UTF8")
                arduino.write(cmd)
                print(cmd)

            prevIsInHitRange = nextIsInHitRange

            cv2.imshow('Frame', frame)
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
