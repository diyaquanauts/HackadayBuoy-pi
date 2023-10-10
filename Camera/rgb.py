#! /Users/brett/opt/anaconda3/envs/opencv/bin/python

import cv2
import numpy as np

print(cv2.__version__)

cap = cv2.VideoCapture("tre.mp4")

if not cap.isOpened():
    print("Error opening video file")
    exit()

ret, frame = cap.read()

if not ret:
    print("Error reading frame")
    exit()

fgbg_b = cv2.createBackgroundSubtractorKNN(history=500, detectShadows=False, dist2Threshold =50)
fgbg_g = cv2.createBackgroundSubtractorKNN(history=500, detectShadows=False, dist2Threshold =50)
fgbg_r = cv2.createBackgroundSubtractorKNN(history=500, detectShadows=False, dist2Threshold =50)

blur_level = 3
while True:

    b, g, r = cv2.split(frame)

    fgmask_b = fgbg_b.apply(b)
    fgmask_g = fgbg_g.apply(g)
    fgmask_r = fgbg_r.apply(r)

    # Display the frame
    cv2.imshow("Blue Channel", b)
    cv2.imshow("Green Channel", g)
    cv2.imshow("Red Channel", r)

    # Wait for key press
    key = cv2.waitKey(1) & 0xFF

    # If 'q' is pressed, exit the loop
    if key == ord('q'):
        break

    # Read the next frame
    ret, frame = cap.read()

    # Check if the frame is read correctly
    if not ret:
        print("Error reading frame")
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
