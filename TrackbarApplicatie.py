#
# Playback video en in een loop
#
import cv2

# Variable die
h_upper = 0

def on_h_upper(val):
    global h_upper
    h_upper = val

cv2.namedWindow("Trackbar")
cv2.createTrackbar('H upper', 'Trackbar', 0, 255, on_h_upper )

#
while True:
    # Als done = True -> exit
    done = False

    # Probeer video in te lezen en exit() als dit niet lukt
    capture = cv2.VideoCapture('resources/sample_video.mp4')
    if capture.isOpened() == False:
        print("Error opening video !")
        exit()

    # Playback video ...
    while capture.isOpened():

        # Grap frame by frame if possible
        ret, frame = capture.read()

        # Break als video af is gelopen
        if ret == True:

            #  ... hier komt dan de Computer Vision applicatie ..

            #
            cv2.imshow("Frame", frame)

            #  ... q = quit() ...
            if cv2.waitKey(10) & 0xFF == ord('q'):
                done = True
                break
        else:
            break
    if done:
        break

# Alles klaar. Release capture object
capture.release()
cv2.destroyAllWindows()


