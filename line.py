import typing

import cv2
import numpy as np

def velocity(t):
    return t**2 / 100

origin = np.array([0, 0])
direction = np.array([1, 1])
direction = direction / np.linalg.norm(direction)

origin2 = np.array([400, 401])
direction2 = np.array([414, 373]) - origin2
direction2 = direction2 / np.linalg.norm(direction2)

window_name = "Line"
cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

frame_cnt = 0
while True:
    key = cv2.waitKey(10)
    if key == 27:
        break
    
    if key == ord('b'):
        frame_cnt -= 1
    elif key == ord('p'):
        frame_cnt += 1
    elif key == ord('r'):
        frame_cnt = 0

    image = np.zeros((480, 640, 3), dtype=np.uint8)

    tt = np.clip(frame_cnt, 0, 56)
    length = 0
    for t in range(tt): length += velocity(t)
    cv2.line(image, 
        tuple(origin.astype(np.int32)),  
        tuple((origin + length * direction).astype(np.int32)), 
        (255, 255, 255), 
        3)

    if frame_cnt >= 120:
        tt = np.clip(frame_cnt - 120, 0, 20)
        length = 0
        for t in range(tt): length += velocity(t)
        cv2.line(image, 
            tuple(origin2.astype(np.int32)),  
            tuple((origin2 + length * direction2).astype(np.int32)), 
            (255, 255, 255), 
            3)
    
    cv2.circle(image, (414, 373), 8, (0, 0, 255), -1)

    cv2.putText(image, 
        f"{frame_cnt}", 
        (0, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
    cv2.imshow(window_name, image)
