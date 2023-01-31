import numpy as np
import cv2

# detect all connected webcams
valid_cams = []
for i in range(8):
    cap = cv2.VideoCapture(i)
    if cap is None or not cap.isOpened():
        print('Warning: unable to open video source: ', i)
    else:
        valid_cams.append(i)

print(valid_cams)
