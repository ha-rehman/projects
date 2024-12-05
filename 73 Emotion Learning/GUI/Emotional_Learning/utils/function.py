import os
import datetime
import random
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import time


def text_drawing(frame, label, last_call_time):
    text = f"Last Detected Emotion is {label} at {last_call_time}"
    # Define the position where the text will be placed (x, y)
    x, y = 50, 50  # Adjust these coordinates as needed

    # Define the font type, scale, color, and thickness
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (0, 255, 0)  # BGR color format (green in this case)
    font_thickness = 2

    # Split the text into lines to fit within the frame width
    max_width = 300  # Adjust this value based on your frame width
    lines = []
    line = ""
    for word in text.split():
        test_line = line + " " + word if line else word
        text_size = cv2.getTextSize(test_line, font, font_scale, font_thickness)[0]
        if text_size[0] <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)

    # Use cv2.putText to draw each line of text on the frame
    line_height = int(text_size[1] * 1.5)  # Adjust the line height
    for i, line in enumerate(lines):
        y_offset = y + i * line_height
        cv2.putText(frame, line, (x, y_offset), font, font_scale, font_color, font_thickness)

    return frame


def generate_session_id(request):
    # Get the first 4 characters of the user ID
    user_id = request.user.id
    print(user_id)
    # user_id_prefix = user_id[:4]

    # Get the current date and format it as YYYYMMDD
    current_date = datetime.datetime.now().strftime('%Y%m%d')

    # Generate 4 random numbers between 1000 and 9999
    random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(4))

    # Join the components with hyphens
    session_id = f'{user_id}-{current_date}-{random_numbers}'

    return session_id


def predictor(frame):
    # Load the model
    base_path = os.getcwd()
    model_path = os.path.join(base_path, "utils", "keras_model.h5")
    model = load_model(model_path, compile=False)

    # Load the labels
    class_names = ['bored', 'frustrated', 'drowsy', 'engaged', 'looking away', 'confused']

    # Resize the raw image into (224-height, 224-width) pixels
    image = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)

    # Make the image a numpy array and reshape it to the model's input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predict the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    # print("Class:", class_name, end="")
    return class_name
