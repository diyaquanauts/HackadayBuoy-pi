#! /Users/brett/opt/anaconda3/bin/python
import cv2
import numpy as np
import os

cam = cv2.VideoCapture('trim480.mov')
fgbg = cv2.createBackgroundSubtractorMOG2()
print(cv2.__version__)

# Define output video settings
fps = int(cam.get(cv2.CAP_PROP_FPS))
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_file = cv2.VideoWriter('output.mp4', fourcc, fps, (frame_width, frame_height), isColor=True)

frame_count = 0
while True:
    check, frame = cam.read()
    if check:
        fgmask = fgbg.apply(frame)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, (10,10))
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, (10,10))

        contours, hierarchy = cv2.findContours(fgmask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        count = 0
        for c in contours:
            (x, y), radius = cv2.minEnclosingCircle(c)
            center = (int(x), int(y))
            radius = int(radius)
            if(radius > 3):
                count += 1
                cv2.circle(frame,center,radius+4,(0,255,0),1)

        colormask = cv2.bitwise_and(frame, frame, mask=fgmask)
        cv2.imshow('MASKED', frame)

        # Write the current frame to the output video file
        output_file.write(frame)

        key = cv2.waitKey(1)
        if key == 27:
            break

        frame_count += 1

cam.release()
output_file.release()
cv2.destroyAllWindows()
