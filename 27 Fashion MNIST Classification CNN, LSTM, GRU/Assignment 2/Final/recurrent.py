import argparse
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow import keras
from tensorflow.keras import layers
from matplotlib import pyplot as plt


def prepare_dataset(csv, sequence_len):
    df = pd.read_csv(csv)
    temperature = df['T (degC)']
    temperature = list(temperature)

    plt.plot(range(len(temperature)), temperature)

    plt.plot(range(1440), temperature[:1440])

    raw_data = df.iloc[:,1:]

    num_train_samples = int(0.5 * len(raw_data))
    num_val_samples = int(0.25 * len(raw_data))
    num_test_samples = len(raw_data) - num_train_samples - num_val_samples
    print("num_train_samples:", num_train_samples)
    print("num_val_samples:", num_val_samples)
    print("num_test_samples:", num_test_samples)

    mean = raw_data[:num_train_samples].mean(axis=0)
    raw_data -= mean
    std = raw_data[:num_train_samples].std(axis=0)
    raw_data /= std


    sampling_rate = 6
    sequence_length = sequence_len
    delay = sampling_rate * (sequence_length + 24 - 1)
    batch_size = 256

    train_dataset = keras.preprocessing.timeseries_dataset_from_array(
        raw_data[:-delay],
        targets=temperature[delay:],
        sampling_rate=sampling_rate,
        sequence_length=sequence_length,
        shuffle=True,
        batch_size=batch_size,
        start_index=0,
        end_index=num_train_samples)

    val_dataset = keras.preprocessing.timeseries_dataset_from_array(
        raw_data[:-delay],
        targets=temperature[delay:],
        sampling_rate=sampling_rate,
        sequence_length=sequence_length,
        shuffle=True,
        batch_size=batch_size,
        start_index=num_train_samples,
        end_index=num_train_samples + num_val_samples)

    test_dataset = keras.preprocessing.timeseries_dataset_from_array(
        raw_data[:-delay],
        targets=temperature[delay:],
        sampling_rate=sampling_rate,
        sequence_length=sequence_length,
        shuffle=True,
        batch_size=batch_size,
        start_index=num_train_samples + num_val_samples)

    return raw_data, train_dataset, val_dataset, test_dataset


def train_LSTM(raw_data, train_dataset, val_dataset, test_dataset, sequence_length):
    inputs = keras.Input(shape=(sequence_length, raw_data.shape[-1]))
    x = layers.LSTM(32, recurrent_dropout=0.25)(inputs)
    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(1)(x)
    model = keras.Model(inputs, outputs)

    saved_model_name = "jena_lstm_dropout_{}.keras".format(sequence_length)
    callbacks = [
        keras.callbacks.ModelCheckpoint(saved_model_name,
                                        save_best_only=True)
    ]
    model.compile(optimizer="rmsprop", loss="mse", metrics=["mae"])
    history = model.fit(train_dataset,
                        epochs=50,
                        validation_data=val_dataset,
                        callbacks=callbacks)

    model = keras.models.load_model(saved_model_name)
    print(f"Test MAE: {model.evaluate(test_dataset)[1]:.2f}")


def train_GRU(raw_data, train_dataset, val_dataset, test_dataset, sequence_length):
    inputs = keras.Input(shape=(sequence_length, raw_data.shape[-1]))
    x = layers.GRU(32, recurrent_dropout=0.5, return_sequences=True)(inputs)
    x = layers.GRU(32, recurrent_dropout=0.5)(x)
    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(1)(x)
    model = keras.Model(inputs, outputs)

    saved_model_name = "jena_stacked_gru_dropout_{}.keras".format(sequence_length)

    callbacks = [
        keras.callbacks.ModelCheckpoint(saved_model_name,
                                        save_best_only=True)
    ]
    model.compile(optimizer="rmsprop", loss="mse", metrics=["mae"])
    history = model.fit(train_dataset,
                        epochs=50,
                        validation_data=val_dataset,
                        callbacks=callbacks)

    model = keras.models.load_model(saved_model_name)
    print(f"Test MAE: {model.evaluate(test_dataset)[1]:.2f}")




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--d', required=True)
    args = parser.parse_args()

    sequence_length = 120
    raw_data, train_dataset, val_dataset, test_dataset = prepare_dataset(args['d'], sequence_length)

    train_LSTM(raw_data, train_dataset, val_dataset, test_dataset)
    train_GRU(raw_data, train_dataset, val_dataset, test_dataset)
