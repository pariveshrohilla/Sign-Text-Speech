import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)

print("=== TIGHT HAND BORDER DETECTOR ===")
print("1=Border | 2=Landmarks | 3=Dots | Q=Quit")

mode = 1  # Start with border mode

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    image = frame.copy()
    
    if results.multi_hand_landmarks:
        for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            h, w, _ = image.shape
            
            # === MODE 1: TIGHT HAND BORDER ===
            if mode == 1:
                x_coords = [lmk.x * w for lmk in hand_landmarks.landmark]
                y_coords = [lmk.y * h for lmk in hand_landmarks.landmark]
                x_min, x_max = int(min(x_coords)), int(max(x_coords))
                y_min, y_max = int(min(y_coords)), int(max(y_coords))
                
                # MINIMAL padding = JUST around hand
                padding = 8
                cv2.rectangle(image, 
                            (x_min-padding, y_min-padding), 
                            (x_max+padding, y_max+padding),
                            (0, 255, 0), 3)  # Thin, tight green border
                
                cv2.putText(image, f'Hand {hand_idx+1}', (x_min, y_min-padding-5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # ROI dimensions
                roi_w = x_max - x_min + padding*2
                roi_h = y_max - y_min + padding*2
                cv2.putText(image, f'{roi_w}x{roi_h}px', (x_min, y_max+padding+15),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            # === MODE 2: FULL LANDMARKS ===
            elif mode == 2:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0,255,255), thickness=3, circle_radius=5),
                    mp_drawing.DrawingSpec(color=(255,0,255), thickness=3))
            
            # === MODE 3: DOTS ONLY ===
            elif mode == 3:
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    color = (0, 255, 0) if idx < 5 else (0, 0, 255)
                    cv2.circle(image, (x, y), 8, color, -1)
                    cv2.putText(image, str(idx), (x+8, y-8),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
    
    # Mode display
    mode_names = {1: "TIGHT BORDER", 2: "LANDMARKS", 3: "DOTS"}
    cv2.putText(image, f"MODE: {mode_names[mode]} (1/2/3)", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    cv2.imshow('Tight Hand Detector', image)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break
    elif key == ord('1'): mode = 1; print("🔲 Tight border")
    elif key == ord('2'): mode = 2; print("🎨 Landmarks")  
    elif key == ord('3'): mode = 3; print("● Dots")

cap.release()
cv2.destroyAllWindows()