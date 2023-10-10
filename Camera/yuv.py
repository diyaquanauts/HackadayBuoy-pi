#! /Users/brett/opt/anaconda3/envs/opencv/bin/python

import cv2
import numpy as np

def simplest_cb(img, percent=1):
    assert img.shape[2] == 3
    assert percent > 0 and percent < 100

    half_percent = percent / 200.0

    channels = cv2.split(img)

    out_channels = []
    for channel in channels:
        assert len(channel.shape) == 2
        # find the low and high precentile values (based on the input percentile)
        height, width = channel.shape
        vec_size = width * height
        flat = channel.reshape(vec_size)

        assert len(flat.shape) == 1

        flat = np.sort(flat)

        n_cols = flat.shape[0]

        low_val  = flat[int(np.floor(n_cols * half_percent))]
        high_val = flat[int(np.ceil( n_cols * (1.0 - half_percent)))]

        # saturate below the low percentile and above the high percentile
        thresholded = channel.copy()
        thresholded[thresholded < low_val] = low_val
        thresholded[thresholded > high_val] = high_val

        # scale the channel
        normalized = cv2.normalize(thresholded, thresholded.copy(), 0, 255, cv2.NORM_MINMAX)
        out_channels.append(normalized)

    return cv2.merge(out_channels)


print(cv2.__version__)
cap = cv2.VideoCapture("tre.mp4")
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Be sure to use lower case

if not cap.isOpened():
    print("Error opening video file")
    exit()

ret, frame = cap.read()

if not ret:
    print("Error reading frame")
    exit()

fgbg_y = cv2.createBackgroundSubtractorKNN(
    history=100,
    detectShadows=False,
    dist2Threshold=350)

out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame.shape[1], frame.shape[0]), True)

while True:
    og = np.copy(frame)
    og = simplest_cb(og,1)

    frame[:, :, 2] = 0
    yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
    y, u, v = cv2.split(yuv)

    fgmask = fgbg_y.apply(cv2.equalizeHist(y))

    # kernel_size = 3  # you can change this value
    # kernel = np.ones((kernel_size, kernel_size), np.uint8)
    # fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    # kernel_size = 10  # you can change this value
    # kernel = np.ones((kernel_size, kernel_size), np.uint8)
    # fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)

    # Convert the grayscale frame to three channels
    frame_gray = cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)

    # Create a mask in three channels
    fgmask_3 = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR)

    # Mask the colored image with the fgmask
    frame_colored_masked = cv2.bitwise_and(og, og, mask=fgmask)

    # Mask the grayscale image with the inverse of the fgmask
    frame_gray_masked = cv2.bitwise_and(frame_gray, frame_gray, mask=cv2.bitwise_not(fgmask))

    # Add the two masked images
    combined_frame = cv2.add(frame_colored_masked, frame_gray_masked)

    out.write(combined_frame)

    # Display the frame
    cv2.imshow("Combined Frame", combined_frame)

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
out.release()
cv2.destroyAllWindows()
