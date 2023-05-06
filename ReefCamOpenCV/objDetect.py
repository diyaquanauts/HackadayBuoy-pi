#! /Users/brett/opt/anaconda3/bin/python
import cv2

# Initialize the video stream
cam = cv2.VideoCapture("test1080.mov")

# Define the ROI (Region of Interest) for the object to track
ret, frame = cam.read()
bbox = cv2.selectROI("SELECT ROI", frame, False)

# Initialize the tracker with the ROI
tracker = cv2.TrackerMIL_create()
tracker.init(frame, bbox)

# Initialize a list to store the center points of the bounding box
points = []

while True:
    # Read a frame from the video stream
    ret, frame = cam.read()
    if not ret:
        break

    # Update the tracker with the new frame
    success, bbox = tracker.update(frame)

    # If the tracking was successful, draw the bounding box around the object
    if success:
        left, top, w, h = [int(i) for i in bbox]
        right, bottom = left + w, top + h
        center_x, center_y = int(left + w/2), int(top + h/2)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Append the center point to the list
        points.append((center_x, center_y))

        # Draw the trail as a red line from the center points
        for i in range(1, len(points)):
            cv2.line(frame, points[i-1], points[i], (0, 0, 255), 2)

    # Show the frame with the bounding box and trail drawn
    cv2.imshow("FRAME", frame)

    # Wait for a key press and exit if the 'Esc' key is pressed
    key = cv2.waitKey(1)
    if key == 27:
        break

# Release the video stream and close all windows
cam.release()
cv2.destroyAllWindows()
