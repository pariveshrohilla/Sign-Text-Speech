import cv2
import numpy as np
import mediapipe as mp
from function import *
from keras.models import model_from_json

# Load model
with open("model.json", "r") as json_file:
    model = model_from_json(json_file.read())
model.load_weights("model.h5")

# Mediapipe
mp_hands = mp.solutions.hands

# IMPORTANT: make sure these exist in your trained model
# Example:
# actions = np.array(['A','B','C',...,'SPACE','DEL','CLEAR'])

# Detection variables
sequence = []
predictions = []
threshold = 0.8

# Word builder variables
current_word = ""
last_added = ""
cooldown = 0

# Camera
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # ROI
        cropframe = frame[40:400, 0:300]
        cv2.rectangle(frame, (0, 40), (300, 400), (255, 0, 0), 2)

        # Detection
        image, results = mediapipe_detection(cropframe, hands)

        keypoints = extract_keypoints(results)
        sequence.append(keypoints)
        sequence = sequence[-30:]

        current_label = "-"
        current_conf = 0

        try:
            if len(sequence) == 30:
                res = model.predict(np.expand_dims(sequence, axis=0))[0]
                pred_class = np.argmax(res)

                current_label = actions[pred_class]
                current_conf = res[pred_class] * 100

                predictions.append(pred_class)

                # Smooth prediction
                if len(predictions) > 10:
                    most_common = max(set(predictions[-10:]),
                                      key=predictions[-10:].count)

                    if most_common == pred_class and res[pred_class] > threshold:

                        predicted_char = actions[pred_class]

                        # Add character with cooldown
                        if cooldown == 0 and predicted_char != last_added:

                            if predicted_char == "SPACE":
                                current_word += " "
                            elif predicted_char == "DEL":
                                current_word = current_word[:-1]
                            elif predicted_char == "CLEAR":
                                current_word = ""
                            else:
                                current_word += predicted_char

                            last_added = predicted_char
                            cooldown = 15  # adjust typing speed

        except Exception:
            pass

        # Reduce cooldown
        if cooldown > 0:
            cooldown -= 1

        # ---------------- UI ---------------- #

        # Top blue bar
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (255, 0, 0), -1)
        header_text = f"Current: {current_label} ({current_conf:.2f}%)"
        cv2.putText(frame, header_text, (10, 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (255, 255, 255), 2, cv2.LINE_AA)

        # Bottom black bar
        cv2.rectangle(frame,
                      (0, frame.shape[0] - 40),
                      (frame.shape[1], frame.shape[0]),
                      (0, 0, 0), -1)

        bottom_text = f"Word: {current_word}"
        cv2.putText(frame, bottom_text,
                    (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (255, 255, 255), 2, cv2.LINE_AA)

        # Show
        cv2.imshow('OpenCV Feed', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()