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

print("not damaged : ")
for i in range(52):
    print("i = ",i+1,classify_image("roofs/not_damaged/"+str(i+1)+".png"))

print("damaged : ")
for i in range(53):
    print("i = ",i+1,classify_image("roofs/damaged/"+str(i+1)+".png"))




