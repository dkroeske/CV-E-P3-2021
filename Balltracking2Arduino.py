# Playback video
import math

import cv2
import serial

# Connection to Arduino
arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)

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
            print( '({},{})'.format( int(x), int(y) ) )

            # Check is (x,y) is in circle
            xc = 560
            yc = 770
            radius = 30
            dist = math.sqrt( math.pow(xc-x,2) + math.pow(yc-y,2))
            if dist < radius:
                cv2.circle(frame, (int(xc), int(yc)), int(radius), (0, 0, 255), -1)
                arduino.write("FIRE")
                ack = arduino.readline()
                while ack != 'OK':
                    ack = arduino.readline()
            else:
                cv2.circle(frame, (int(xc), int(yc)), int(radius), (0, 0, 0), -1)

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
