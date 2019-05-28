import dataclasses
import typing

import cv2
import numpy as np

def func(t):
    t = np.clip(t, 0., 1.)
    a = 0.9
    if t < a:
        x = t ** 2 / a
    else:
        x = 1 - (1 - t) ** 2 / (1 - a)

    return x

@dataclasses.dataclass
class Triangle:
    top: np.ndarray
    left: np.ndarray
    right: np.ndarray
    scale: float
    color: typing.Tuple

    def draw(self, image, center):
        cv2.fillConvexPoly(image, 
            np.array([
                center + self.scale * self.top, 
                center + self.scale * self.left, 
                center + self.scale * self.right
            ]).astype(np.int32), 
            self.color)

    def interpolate(src, dst, t):
        s = func(t)
        return Triangle(
            top = src.top * (1 - s) + dst.top * s, 
            left = src.left * (1 - s) + dst.left * s, 
            right = src.right * (1 - s) + dst.right * s, 
            scale = src.scale * (1 - s) + dst.scale * s, 
            color = tuple(np.array(list(src.color)) * (1 - s) + np.array(list(dst.color)) * s), 
        )

society = Triangle(
    top    = np.array([   0, -0.5]), 
    left   = np.array([-0.5,  0.5]), 
    right  = np.array([ 0.5,  0.5]), 
    scale  = 50,
    color = (255, 255, 255), 
)

me = Triangle(
    top    = np.array([-0.3,  0.1]), 
    left   = np.array([-0.8,  0.9]), 
    right  = np.array([ 0.1,  0.8]), 
    scale  = 50,
    color = (226, 102, 255), 
)


frame_cnt = 0
window_name = "Triangle"
cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

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
    fuck = Triangle.interpolate(me, society, frame_cnt / 100)
    
    for j in [140, 240, 340]:
        for i in [120, 220, 320, 420, 520]:
            if j == 240 and i == 420:
                fuck.draw(image, np.array([i, j]))
            else:
                society.draw(image, np.array([i, j]))

    cv2.putText(image, 
        f"{frame_cnt}", 
        (0, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
    cv2.imshow(window_name, image)
