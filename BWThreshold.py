import cv2

img = cv2.imread('resources/threshold.png')

# Blur (onscherp maken -> ruis filteren)
blur = cv2.blur(img, (3,3) )

# Thresholding (drempel)
ret, threshold = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)

#
edges = cv2.Canny(threshold, 100, 200)


cv2.imshow('Origineel', img)
cv2.imshow('Blur', blur)
cv2.imshow('Threshold', threshold)
cv2.imshow('edges', edges)


while(1):
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break