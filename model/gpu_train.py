import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from datetime import datetime
from os import listdir
from os.path import isfile, join

x = np.load("x.npy")
y = np.load("y.npy")

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.1, random_state=42
)

while True:
    model_name = sorted([f for f in listdir("models") if isfile(join("models", f))])[-1]
    model = tf.keras.models.load_model(f"models/{model_name}")
    model.compile(optimizer="adam", loss="mean_squared_error", metrics=["mae"])
    model.fit(
        x_train, y_train, epochs=1, batch_size=64, validation_data=(x_test, y_test)
    )
    model.save(f"models/{datetime.today().strftime('%Y-%m-%d_%H-%M-%S')}.keras")
