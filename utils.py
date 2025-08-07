import math

def distance_2d(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.hypot(x2 - x1, y2 - y1)

def is_extended(tip_y, pip_y, mcp_y) -> bool:
    return tip_y < pip_y < mcp_y

def is_index_pointing(hand_landmarks) -> bool:
    index_tip = hand_landmarks.landmark[8].y
    index_pip = hand_landmarks.landmark[6].y
    index_mcp = hand_landmarks.landmark[5].y

    middle_tip = hand_landmarks.landmark[12].y
    ring_tip = hand_landmarks.landmark[16].y
    pinky_tip = hand_landmarks.landmark[20].y

    return (
        is_extended(index_tip, index_pip, index_mcp) and
        middle_tip > hand_landmarks.landmark[10].y and
        ring_tip > hand_landmarks.landmark[14].y and
        pinky_tip > hand_landmarks.landmark[18].y
    )