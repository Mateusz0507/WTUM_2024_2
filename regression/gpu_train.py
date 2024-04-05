import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
import base64
from datetime import datetime
from os import listdir
from os.path import isfile, join


data = pd.read_csv("data/parsed_data2-6.csv")

X = np.array(
    [
        np.frombuffer(base64.b64decode(board), dtype=np.bool_).reshape((6, 7, 2))
        for board in data["board"]
    ]
)
y = data["evaluation"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


while True:
    model_name = sorted(
        [f for f in listdir("models/fromdata2") if isfile(join("models/fromdata2", f))]
    )[-1]
    model = tf.keras.models.load_model(f"models/fromdata2/{model_name}")
    model.compile(optimizer="adam", loss="mean_squared_error", metrics=["mae"])
    model.fit(
        X_train, y_train, epochs=1, batch_size=64, validation_data=(X_test, y_test)
    )
    model.save(
        f"models/fromdata2/{datetime.today().strftime('%Y-%m-%d_%H-%M-%S')}.keras"
    )
