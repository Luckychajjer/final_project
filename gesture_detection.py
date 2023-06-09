import cv2
import tkinter as tk
import mediapipe as mp
from PIL import ImageTk, Image

# Initialize Mediapipe hands module
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Gesture detection constants
SWIPE_LEFT = "Swipe Left"
SWIPE_RIGHT = "Swipe Right"
SWIPE_UP = "Swipe UP"
SWIPE_DOWN = "Swipe DOWN"
GESTURE_THRESHOLD = 50

# Initialize variables
prev_x = 0
curr_x = 0
prev_y = 0
curr_y = 0
gesture = None



# Initialize video capture
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5) as hands:

    while cap.isOpened():
        # Read video feed
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)

        # Convert the BGR frame to RGB for Mediapipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with Mediapipe
        results = hands.process(frame_rgb)


        # Check if hands are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get the x-coordinate of the index finger tip
                curr_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * frame.shape[1])
                curr_y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * frame.shape[0])
                
                # Calculate the x-coordinate difference
                delta_x = curr_x - prev_x
                delta_y = curr_y - prev_y

                if abs(delta_x) > abs(delta_y):
                    if delta_x > GESTURE_THRESHOLD:
                         gesture = SWIPE_RIGHT
                    elif delta_x < -GESTURE_THRESHOLD:
                        gesture = SWIPE_LEFT
                
                elif abs(delta_x) < abs(delta_y):
                    if delta_y > GESTURE_THRESHOLD:
                         gesture = SWIPE_DOWN
                    elif delta_y < -GESTURE_THRESHOLD:
                        gesture = SWIPE_UP

                # Detect swipe gestures
                

                # Update previous x-coordinate
                prev_x = curr_x
                prev_y = curr_y
                # Draw hand landmarks on the frame
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Display gesture text on the frame
        cv2.putText(frame, gesture, (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0), 2)

        # Display the resulting frame
        cv2.imshow('Gesture Control', frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
