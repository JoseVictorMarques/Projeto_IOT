import tensorflow
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.optimizers import SGD
from keras.utils import to_categorical
import numpy as np
from cv2 import cv2
import os
import random
from sklearn.model_selection import train_test_split


img_folder = "roofs/damaged"
images = []
labels = []

for filename in os.listdir(img_folder):
    image = cv2.imread(os.path.join(img_folder,filename))
    if image is not None:
        image = cv2.resize(image,(32,32)).flatten()
        images.append(image)
        labels.append(1)


img_folder = "roofs/not_damaged"

for filename in os.listdir(img_folder):
    image = cv2.imread(os.path.join(img_folder,filename))
    if image is not None:
        image = cv2.resize(image,(32,32)).flatten()
        images.append(image)
        labels.append(0)


c = list(zip(images, labels))

random.shuffle(c)

images, labels = zip(*c)

images = np.array(images, dtype = "float") / 255.0
labels = np.array(labels)

(x_train , x_test , y_train , y_test) = train_test_split(images, labels, test_size =  0.15 , random_state = 42)


y_train_one_hot = to_categorical(y_train)
y_test_one_hot = to_categorical(y_test)

#model

model = Sequential()
model.add(Dense(1024, input_shape=(3072,), activation="sigmoid"))
model.add(Dense(512, activation="sigmoid"))
model.add(Dense(2, activation="softmax"))

###
INIT_LR = 0.01
EPOCHS = 80

opt = SGD(lr=INIT_LR)
model.compile(loss="categorical_crossentropy", optimizer=opt,metrics=["accuracy"])


H = model.fit(x=x_train, y=y_train_one_hot, validation_data=(x_test, y_test_one_hot),epochs=EPOCHS, batch_size=32)

print("[INFO] serializing network and label binarizer...")
model.save("model")
