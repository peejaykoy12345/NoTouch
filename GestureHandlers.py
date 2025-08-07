import mediapipe as mp
import pyautogui
from utils import distance_2d, is_extended, is_index_pointing

pyautogui.FAILSAFE = False

screen_width, screen_height = pyautogui.size()

def handle_move_movements(hand_landmarks) -> None:
    global screen_width, screen_height
    index_tip = hand_landmarks.landmark[8]

    middle_finger_tip = hand_landmarks.landmark[12].y
    middle_finger_pip = hand_landmarks.landmark[10].y
    middle_finger_mcp = hand_landmarks.landmark[9].y

    is_pointing = is_index_pointing(hand_landmarks) and not is_extended(middle_finger_tip, middle_finger_pip, middle_finger_mcp)

    if is_pointing:
        x_pos, y_pos = index_tip.x * screen_width, index_tip.y * screen_height
        print(f"Position to move to {x_pos}, {y_pos}")
        pyautogui.moveTo(x_pos, y_pos)

has_m1 = False

def handle_m1(hand_landmarks) -> None:
    global has_m1

    pinky_tip = hand_landmarks.landmark[20].y
    pinky_mcp = hand_landmarks.landmark[17].y
    pinky_pip = hand_landmarks.landmark[18].y

    is_pinky_extended = is_extended(pinky_tip, pinky_pip, pinky_mcp)

    if not has_m1 and is_pinky_extended:
        pyautogui.click()
        has_m1 = True

    if has_m1 and not is_pinky_extended:
        has_m1 = False

past_middle_tip_y = None

SCROLL_SENSETIVITY = 2000

def handle_mousescroll(hand_landmarks) -> None:
    global past_middle_tip_y

    ring_tip = hand_landmarks.landmark[16].y
    ring_pip = hand_landmarks.landmark[14].y
    ring_mcp = hand_landmarks.landmark[13].y

    is_ring_extended = is_extended(ring_tip, ring_pip, ring_mcp)

    if is_ring_extended:
        past_middle_tip_y = None
        return

    index_tip = hand_landmarks.landmark[8].y
    index_pip = hand_landmarks.landmark[6].y
    index_mcp = hand_landmarks.landmark[5].y

    middle_finger_tip = hand_landmarks.landmark[12].y
    middle_finger_pip = hand_landmarks.landmark[10].y
    middle_finger_mcp = hand_landmarks.landmark[9].y

    # Check if both the middle finger and index is extended
    is_gestured = is_extended(index_tip, index_pip, index_mcp) and is_extended(middle_finger_tip, middle_finger_pip, middle_finger_mcp)

    print(f"Is gestured? {is_gestured}")

    if not is_gestured:
        past_middle_tip_y = None
        return

    if past_middle_tip_y is None:
        past_middle_tip_y = middle_finger_tip

    # Get the difference between the middle finger now and before to check for movement
    difference = middle_finger_tip - past_middle_tip_y

    print(f"Difference: {difference}")

    if abs(difference) < 0.06: return

    past_middle_tip_y += (middle_finger_tip - past_middle_tip_y) * 0.2

    past_middle_tip_y = middle_finger_tip

    scroll_amount = int(difference * SCROLL_SENSETIVITY)

    print(f"Scroll amount: {scroll_amount}")

    pyautogui.scroll(scroll_amount)






