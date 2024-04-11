import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
from datetime import datetime

model = tf.keras.Sequential(
    [
        Dense(units=1, input_shape=[2, 3]),
        Dense(units=12, input_shape=[1]),
        Dense(units=6, input_shape=[1]),
        Dense(units=2, input_shape=[1]),
        Dense(units=1, input_shape=[1]),
    ]
)
model.compile(optimizer="adam", loss="mean_squared_error", metrics=["mae"])
model.summary()

model.save(f"models/{datetime.today().strftime('%Y-%m-%d_%H-%M-%S')}.keras")
