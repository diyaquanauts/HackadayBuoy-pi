#! /Users/brett/opt/anaconda3/envs/opencv/bin/python
import cv2
import numpy as np

def onThreshold(val):
    global threshold
    threshold = val

def onShadow(val):
    global shadow
    if(val == 0):
        shadow = False
    else:
        shadow = True

def on_trackbar(val):
    global blur_level
    blur_level = val

def onEqHist(val):
    global shouldEq
    shouldEq = val

def onRed(val):
    global shouldRed
    shouldRed = val

def onClahe(val):
    global shouldClahe
    shouldClahe = val

def onMorphOpen(val):
    global morph_open_size
    morph_open_size = val

def onMorphClose(val):
    global morph_close_size
    morph_close_size = val

cam = cv2.VideoCapture('TRIM.mov')
fgbg = cv2.createBackgroundSubtractorKNN(
    history=500,
    detectShadows=False,
    dist2Threshold =50
)
print(cv2.__version__)

# Define output video settings
fps = int(cam.get(cv2.CAP_PROP_FPS))
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_file = cv2.VideoWriter('output.mp4', fourcc, fps, (frame_width, frame_height), isColor=True)

frame_count = 0

# Create a named window and trackbar
cv2.namedWindow("Input")
cv2.createTrackbar("Morph Close Size", "Input", 1, 100, onMorphClose)
cv2.createTrackbar("Blur Level", "Input", 0, 40, on_trackbar)
#cv2.createTrackbar("Equalize Histogram", "Input", 0, 1, onEqHist)
# cv2.createTrackbar("Apply CLAHE", "Input", 0, 1, onClahe)
cv2.createTrackbar("Morph Open Size", "Input", 1, 100, onMorphOpen)
cv2.createTrackbar("Show With Red", "Input", 0, 1, onRed)


# Load the video
cap = cv2.VideoCapture("TRIM.mov")

# Check if the video file is opened successfully
if not cap.isOpened():
    print("Error opening video file")
    exit()

# Read the first frame
ret, frame = cap.read()

# Check if the frame is read correctly
if not ret:
    print("Error reading frame")
    exit()

# Initialize blur level
blur_level = 0
shouldEq = 0
shouldClahe = 0
morph_open_size = 0
morph_close_size = 0
shouldRed = 0

max_masks = 20  # or however many you want to remember
masks = []
frames = []

# Process the video frames
while True:
    # frames.append(np.copy(frame))
    if(shouldRed == 0):
        frame[:, :, 2] = 0
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.normalize(v, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    normalized_hsv = cv2.merge([h, s, v])
    normalized_frame = cv2.cvtColor(normalized_hsv, cv2.COLOR_HSV2BGR)
    gray = cv2.cvtColor(normalized_frame, cv2.COLOR_BGR2GRAY)
    if(shouldEq == 1):
        gray = cv2.equalizeHist(gray)
    if(shouldClahe == 1):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(20, 20))
        gray = clahe.apply(gray)
    gray = cv2.GaussianBlur(gray, (2*blur_level+1, 2*blur_level+1), 0)

    fgmask = fgbg.apply(gray)

    # fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, np.ones(morph_open_size, np.uint8))
    # fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, np.ones(morph_close_size, np.uint8))

    # 1. Noise Reduction:
    # Morphological opening (erosion followed by dilation)
    kernel_size = morph_open_size  # you can change this value
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    # 2. Fill holes in moving objects:
    # Morphological closing (dilation followed by erosion)
    kernel_size = morph_close_size  # you can change this value
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)

    # 3. Connect broken parts of an object:
    # Dilation (expands the object boundary)
    # kernel_size = 7  # you can change this value
    # kernel = np.ones((kernel_size, kernel_size), np.uint8)
    # fgmask = cv2.dilate(fgmask, kernel, iterations=1)
    # contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #
    # count = 0
    # for c in contours:
    #     (x, y), radius = cv2.minEnclosingCircle(c)
    #     center = (int(x), int(y))
    #     radius = int(radius)
    #     if (radius > 15):
    #         count += 1
    #         cv2.circle(gray, center, radius + 4, (0, 255, 0), 2)
    #

    #
    # # count = 0
    # for c in contours:
    #     (x, y), radius = cv2.minEnclosingCircle(c)
    #     center = (int(x), int(y))
    #     radius = int(radius)
    #     if (radius > 15):
    #         count += 1
    #         cv2.circle(gray, center, radius + 4, (0, 255, 0), 2)

    # masks.append(fgmask)
    # if len(masks) > max_masks:
    #     masks.pop(0)
    #     frames.pop(0)
    # if len(masks) == max_masks:
    #     num_frames = len(frames)
    #
    #     # initialize the result image and the "topmost object" mask
    #     result = np.zeros_like(frames[0])
    #     top_mask = np.zeros_like(masks[0])
    #
    #     for i in reversed(range(num_frames)):
    #         frame = frames[i]
    #         mask = masks[i]
    #
    #         # update the result image where the current mask is "on top"
    #         result[mask > top_mask] = frame[mask > top_mask]
    #
    #         # update the "topmost object" mask
    #         top_mask = np.maximum(top_mask, mask)
    #
    #     # Display the combined masks and frames
    #     cv2.imshow("Combined Masks and Frames", result)
        # # Create a new image which is the sum of all the masks
        # sum_of_masks = np.sum(masks, axis=0)
        #
        # # Now, only keep those blobs that appear in at least X of the last N frames
        # min_presence = 5  # adjust as needed
        # final_mask = ((sum_of_masks >= max_masks) * 255).astype(np.uint8)
        # cv2.imshow("final", final_mask)

    combined_frame = cv2.hconcat([gray, fgmask])

    # Display the frame
    cv2.imshow("Input", combined_frame)

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
