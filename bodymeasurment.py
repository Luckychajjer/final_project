import cv2,ctypes
import mediapipe as mp

user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Initialize webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # Read frame from webcam
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame,1)
    frame_height, frame_width, _ = frame.shape
    aspect_ratio = frame_width / frame_height

    # Calculate new width and height based on screen resolution
    new_width = int(screen_height * aspect_ratio)
    new_height = screen_height

    # Resize the frame to match the screen resolution
    frame = cv2.resize(frame, (new_width, new_height))
    # Convert BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and detect pose landmarks
    results = pose.process(rgb_frame)

    # If landmarks are detected, print left and right shoulder coordinates and draw rectangles
    if results.pose_landmarks:
        left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        # Get the x, y coordinates of left shoulder
        left_shoulder_x, left_shoulder_y = int(left_shoulder.x * frame.shape[1]), int(left_shoulder.y * frame.shape[0])

        # Get the x, y coordinates of right shoulder
        right_shoulder_x, right_shoulder_y = int(right_shoulder.x * frame.shape[1]), int(right_shoulder.y * frame.shape[0])

        # Print shoulder coordinates
        print(f'Right Shoulder: X={left_shoulder_x}, Y={left_shoulder_y}')  #actually right
        print(f'Left Shoulder: X={right_shoulder_x}, Y={right_shoulder_y}') #actually left

        # Draw rectangles around shoulders
        shoulder_rectangle_thickness = 2
        cv2.putText(frame, f'Right ={left_shoulder_x},{left_shoulder_y}',
                    ((left_shoulder_x - 20, left_shoulder_y - 20)), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Left={right_shoulder_x},{right_shoulder_y}',
                    ((right_shoulder_x - 20, right_shoulder_y - 20)), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0), 2, cv2.LINE_AA)
        cv2.rectangle(frame, (left_shoulder_x - 20, left_shoulder_y - 20),
                      (left_shoulder_x + 20, left_shoulder_y + 20), (0, 255, 0), shoulder_rectangle_thickness)
        cv2.rectangle(frame, (right_shoulder_x - 20, right_shoulder_y - 20),
                      (right_shoulder_x + 20, right_shoulder_y + 20), (0, 255, 0), shoulder_rectangle_thickness)

        # Draw landmarks on the frame
        mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Display the frame with landmarks and rectangles
    cv2.namedWindow('Pose Detection', cv2.WND_PROP_FULLSCREEN) #for full screen
    cv2.setWindowProperty('Pose Detection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) # for fullscreen
    cv2.imshow('Pose Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
