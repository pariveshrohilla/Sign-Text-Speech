from function import *
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard
from keras.callbacks import TensorBoard
import os
import numpy as np

label_map = {label: num for num, label in enumerate(actions)}
# print(label_map)
sequences, labels = [], []

for action in actions:
    for sequence in range(no_sequences):
        window = []
        for frame_num in range(sequence_length):
            print(f"Processing action: {action} | Sequence: {sequence} | Frame: {frame_num}")

            file_path = os.path.join(DATA_PATH, action, str(sequence), f"{frame_num}.npy")
            print(f"Loading file: {file_path}")

            res = np.load(file_path, allow_pickle=True)

            print(f"Loaded file shape: {res.shape} | Type: {type(res)}")

            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])

# Add the print statements here
X = np.array(sequences)
y = to_categorical(labels).astype(int)

# Debugging shapes
print(f"Final X shape: {X.shape}")
print(f"Final y shape: {y.shape}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)

log_dir = os.path.join('Logs')
tb_callback = TensorBoard(log_dir=log_dir)

model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30, 63)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))

model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
model.fit(X_train, y_train, epochs=200, callbacks=[tb_callback])
model.summary()

model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)

model.save('model.h5')
