import typing
from datetime import datetime, timedelta

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

frame_cnt = -60

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(
    f"piercing_line.avi", 
    fourcc, 30, (640, 480), True)

delta_time = timedelta()
prev_time = datetime.now()
fps = 30
frame_period = timedelta(milliseconds = 1000 / fps)

while True:
    key = cv2.waitKey(10)
    if key == 27:
        break
    
#    if key == ord('b'):
#        frame_cnt -= 1
#    elif key == ord('p'):
#        frame_cnt += 1
#    elif key == ord('r'):
#        frame_cnt = 0
    
    cur_time = datetime.now()
    delta_time += (cur_time -  prev_time)
    prev_time = cur_time

    while delta_time > frame_period:
        delta_time -= frame_period
        frame_cnt = min(frame_cnt + 1, 1100)
        out.write(image)

    image = np.zeros((480, 640, 3), dtype=np.uint8)

    tt = np.clip(frame_cnt, 0, 56)
    length = 0
    for t in range(tt): length += velocity(t)
    cv2.line(image, 
        tuple(origin.astype(np.int32)),  
        tuple((origin + length * direction).astype(np.int32)), 
        (255, 255, 255), 
        3)

    if frame_cnt >= 180:
        tt = np.clip(frame_cnt - 180, 0, 20)
        length = 0
        for t in range(tt): length += velocity(t)
        cv2.line(image, 
            tuple(origin2.astype(np.int32)),  
            tuple((origin2 + length * direction2).astype(np.int32)), 
            (255, 255, 255), 
            3)
    
    cv2.circle(image, (414, 373), 8, (0, 0, 255), -1)

#    cv2.putText(image, 
#        f"{frame_cnt}", 
#        (0, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
    cv2.imshow(window_name, image)

out.release()
