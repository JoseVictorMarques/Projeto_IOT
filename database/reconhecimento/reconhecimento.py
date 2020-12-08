import numpy as np
import tensorflow
from tensorflow import keras
import cv2

model = keras.models.load_model("model")

def classify_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image,(64,64)).flatten()

    classification = {}

    predictions = model.predict(np.array([image]))[0]

    if(predictions[1] > predictions[0]):
        classification["status"] = "damaged"
        classification["probability"] = predictions[1]
    else:
        classification["status"] = "not_damaged"
        classification["probability"] = predictions[0]

    return classification

#print(classify_image("roofs/damaged/6.png"))



