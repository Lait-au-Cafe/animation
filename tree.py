import math
import dataclasses

import cv2
import numpy as np

@dataclasses.dataclass
class Branch:
    origin: np.ndarray
    direction: np.ndarray
    scale: float
    birthtime: int
    childhood: int
    adolescene: int
    adulthood: int = None


def lifestage(t, bt, ct, at, et):
    if t < bt: return 0

    dt = t - bt
    if dt < ct: return dt

    dt = dt - ct
    if dt < at: return ct

    dt = dt - at
    if et is None:
        if dt < ct: return (ct - dt)
    else:
        if dt < et: return (ct - dt)
        return (ct - et)

    return 0

angle = math.radians(60)
rot = np.array([
    [math.cos(angle), -math.sin(angle)], 
    [math.sin(angle),  math.cos(angle)]
])

biotree = [
    # 0
    Branch(
        origin = np.array([0, 0]), 
        direction = np.array([1, 1]) / np.linalg.norm(np.array([1, -1])), 
        scale = 1.0, 
        birthtime = 0, 
        childhood = 600, 
        adolescene = 20, 
        adulthood = 100,
        ), 
]
biotree.extend([
    # 1
    Branch(
        origin = np.array([34, 33]), 
        direction = rot @ biotree[0].direction, 
        scale = 1.0, 
        birthtime = 90, 
        childhood = 80, 
        adolescene = 80, 
        adulthood = 40,
        ),
    # 2
    Branch(
        origin = np.array([60, 59]), 
        direction = rot.T @ biotree[0].direction, 
        scale = 1.0, 
        birthtime = 110, 
        childhood = 60, 
        adolescene = 1000, 
        ),
    # 3
    Branch(
        origin = np.array([97, 96]), 
        direction = rot @ biotree[0].direction, 
        scale = 1.0, 
        birthtime = 170, 
        childhood = 60, 
        adolescene = 1000, 
        ),
    # 4
    Branch(
        origin = np.array([143, 142]), 
        direction = rot.T @ biotree[0].direction, 
        scale = 1.0, 
        birthtime = 260, 
        childhood = 150, 
        adolescene = 1500, 
        ),
    # 5
    Branch(
        origin = np.array([237, 242]), 
        direction = rot @ biotree[0].direction, 
        scale = 1.0, 
        birthtime = 472, 
        childhood = 200, 
        adolescene = 10, 
        adulthood = 80,
        ),
    # 6
    Branch(
        origin = np.array([328, 323]), 
        direction = rot.T @ biotree[0].direction, 
        scale = 1.0, 
        birthtime = 597, 
        childhood = 200, 
        adolescene = 10, 
        adulthood = 30,
        ),
])
biotree.extend([
    # 7
    Branch(
        origin = np.array([93, 120]), 
        direction = rot.T @ biotree[3].direction, 
        scale = 1.0, 
        birthtime = 220, 
        childhood = 25, 
        adolescene = 1000, 
        ),
    # 8
    Branch(
        origin = np.array([197, 124]), 
        direction = rot.T @ biotree[4].direction, 
        scale = 1.0, 
        birthtime = 430, 
        childhood = 80, 
        adolescene = 1000, 
        ),
    # 9
    Branch(
        origin = np.array([253, 115]), 
        direction = rot @ biotree[4].direction, 
        scale = 1.0, 
        birthtime = 452, 
        childhood = 80, 
        adolescene = 1000, 
        ),
    # 10
    Branch(
        origin = np.array([402, 300]), 
        direction = rot.T @ biotree[6].direction, 
        scale = 1.0, 
        birthtime = 690, 
        childhood = 100, 
        adolescene = 1000, 
        ),
    # 11
    Branch(
        origin = np.array([459, 285]), 
        direction = rot @ biotree[6].direction, 
        scale = 1.0, 
        birthtime = 780, 
        childhood = 150, 
        adolescene = 1000, 
        ),
])
biotree.extend([
    # 12
    Branch(
        origin = np.array([421, 228]), 
        direction = rot @ biotree[10].direction, 
        scale = 1.0, 
        birthtime = 800, 
        childhood = 80, 
        adolescene = 1000, 
        ),
    # 13
    Branch(
        origin = np.array([521, 347]), 
        direction = rot.T @ biotree[11].direction, 
        scale = 1.0, 
        birthtime = 866, 
        childhood = 80, 
        adolescene = 1000, 
        ),
    # 14
    Branch(
        origin = np.array([539, 365]), 
        direction = rot @ biotree[11].direction, 
        scale = 1.0, 
        birthtime = 915, 
        childhood = 80, 
        adolescene = 1000, 
        ),
])
biotree.extend([
    # 15
    Branch(
        origin = np.array([529, 409]), 
        direction = rot.T @ biotree[14].direction, 
        scale = 1.0, 
        birthtime = 990, 
        childhood = 80, 
        adolescene = 1000, 
        ),
])

frame_cnt = 0
selected_points = None

window_name = "Test"
cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
def on_mouse_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global selected_points
        selected_points = [x, y]
        print(f"{frame_cnt}: ({x}, {y})")

cv2.setMouseCallback(window_name, on_mouse_event)

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
    
    for branch in biotree:
        length = lifestage(frame_cnt, 
            branch.birthtime, branch.childhood, branch.adolescene, branch.adulthood)
        if(length > 0):
            cv2.line(image, 
                tuple(branch.origin.astype(np.int32)), 
                tuple((branch.origin + (branch.scale * length) * branch.direction).astype(np.int32)), 
                (255, 255, 255), 3)

    cv2.putText(image, 
        f"{frame_cnt}: {selected_points}", 
        (0, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
    cv2.imshow(window_name, image)
