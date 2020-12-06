import tensorflow
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.optimizers import SGD
from keras.utils import to_categorical
import numpy as np
from cv2 import cv2
import os
from random import shuffle
from sklearn.model_selection import train_test_split

# carregar imagens para o treinamento
def load_images(folder , lbl):
    for filename in os.listdir(img_folder):
        image = cv2.imread(os.path.join(img_folder,filename))
        if image is not None:
            image = cv2.resize(image,(64,64)).flatten()
            images.append(image)
            labels.append(lbl)

images = []
labels = []

img_folder = os.path.join("roofs","damaged")
load_images(img_folder,1)

img_folder = os.path.join("roofs","not_damaged")
load_images(img_folder,0)

# randomizar os arrays de imagens e labels da mesma forma
c = list(zip(images, labels))
shuffle(c)
images, labels = zip(*c)

# converter os objetos em numpy.ndarray ( valores RGB das imagens é dividido por 255 para obtermos floats de 0 a 1)
images = np.array(images, dtype = "float") / 255.0
labels = np.array(labels)

# separar amostras de teste e de treinamento
(x_train , x_test , y_train , y_test) = train_test_split(images, labels, test_size =  0.25 , random_state = 42)
# converter os labels em matrizes binárias
y_train_one_hot = to_categorical(y_train)
y_test_one_hot = to_categorical(y_test)

# modelo simples de rede neural
model = Sequential()
model.add(Dense(120, input_shape=(12288,), activation="sigmoid"))
model.add(Dense(60, activation="sigmoid"))
model.add(Dense(2, activation="softmax"))

# compilar o modelo
INIT_LR = 0.05
EPOCHS = 140
opt = SGD(lr=INIT_LR)
model.compile(loss="binary_crossentropy", optimizer=opt , metrics=["accuracy"])
# treinar a rede neural
H = model.fit(x=x_train, y=y_train_one_hot, validation_data=(x_test, y_test_one_hot),epochs=EPOCHS, batch_size=32)

#salvar o modelo na pasta /model do projeto
print("Saving model...")
model.save("model")
