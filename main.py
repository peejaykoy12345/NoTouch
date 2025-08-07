import cv2
import mediapipe as mp
from pyautogui import size
from GestureHandlers import handle_move_movements, handle_m1, handle_mousescroll

screen_width, screen_height = size()

# Setup MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_face = mp.solutions.face_mesh

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6
) as hands, mp_face.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6
) as face_mesh:

    print("🎥 Tracking hands + facial expressions... Press 'q' to quit.")

    while True:
        success, frame = cap.read()
        if not success:
            print("⚠️ Failed to grab frame.")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # HAND tracking
        hand_results = hands.process(rgb_frame)
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                handle_move_movements(hand_landmarks)
                handle_m1(hand_landmarks)
                handle_mousescroll(hand_landmarks)
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # FACE tracking
        face_results = face_mesh.process(rgb_frame)
        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                # Draw face landmarks
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=mp_face.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(0,255,0), thickness=1)
                )

                # 🧠 Facial gesture detection example:
                # Detect mouth open using landmarks 13 (lower lip) and 14 (upper lip)
                lower_lip = face_landmarks.landmark[13].y
                upper_lip = face_landmarks.landmark[14].y
                mouth_gap = lower_lip - upper_lip

                if mouth_gap > 0.04:
                    print("😮 Mouth is open (do your Alt+F4 magic here)")

        cv2.imshow("🖐️🧠 Hand & Face Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
