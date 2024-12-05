from tensorflow.keras.models import load_model
import cv2
import numpy as np
import time


def predictor(frame):
    # Load the model
    model = load_model("keras_model.h5", compile=False)

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
    result = class_name[2:]
    print("Class:", class_name[2:], end="")
    return result