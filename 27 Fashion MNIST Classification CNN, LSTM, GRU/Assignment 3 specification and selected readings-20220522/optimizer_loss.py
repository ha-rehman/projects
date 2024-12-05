import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tensorflow.keras.utils import to_categorical


def main():
    # import files
    data_train_file = "fashion-mnist_train.csv"
    data_test_file = "fashion-mnist_test.csv"

    # read files csv
    df_train = pd.read_csv(data_train_file)
    df_test = pd.read_csv(data_test_file)

    # data as array in order to reshape them
    train_data = np.array(df_train, dtype='float32')
    test_data = np.array(df_test, dtype='float32')

    print("Train data shape:", train_data.shape)
    print("Test data shape:", test_data.shape)
    print("\n")

    X_train=train_data[:,1:]/255.0
    Y_train=train_data[:,0]
    X_test = test_data[:,1:]/255.0
    Y_test = test_data[:,0]

    print("X_train shape", X_train.shape)
    print("Y_train shape", Y_train.shape)
    print("X_test shape", X_test.shape)
    print("Y_test shape", Y_test.shape, "\n")

    X_train_reshaped = X_train.reshape(X_train.shape[0],*(28,28))
    X_test_reshaped = X_test.reshape(X_test.shape[0],*(28,28))

    X_train_reshaped = X_train.reshape(X_train.shape[0],*(28,28,1))
    X_test_reshaped = X_test.reshape(X_test.shape[0],*(28,28,1))

    optimizers = []
    loss_functions = []
    loss_scores = []
    acc_scores = []
    converg_rates = []

    for opt in ["adagrad", "sgd", "adam", "adadelta"]:
        for loss_fun in ['sparse_categorical_crossentropy', 'categorical_crossentropy', 'huber_loss']:

            print("Optimizer: ", opt, "  Loss Function: ", loss_fun)

            model = models.Sequential()

            model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
            model.add(layers.MaxPool2D((2, 2), strides=1))
            model.add(layers.BatchNormalization())
            model.add(layers.Dropout(0.1))

            model.add(layers.Conv2D(64, (3, 3), activation='relu'))
            model.add(layers.MaxPool2D((2, 2), strides=1))
            model.add(layers.BatchNormalization())
            model.add(layers.Dropout(0.1))

            model.add(layers.Flatten())
            model.add(layers.Dense(10))
            #         model.summary()

            model.compile(optimizer=opt, loss=loss_fun, metrics=['accuracy'])

            if loss_fun == 'sparse_categorical_crossentropy':
                history = model.fit(X_train_reshaped, Y_train, epochs=10, validation_data=(X_test_reshaped, Y_test))
            else:
                history = model.fit(X_train_reshaped, to_categorical(Y_train), epochs=10,
                                    validation_data=(X_test_reshaped, to_categorical(Y_test)))

            # Displaying the model results
            plt.plot(history.history['accuracy'], label='accuracy')
            plt.plot(history.history['val_accuracy'], label='val_accuracy')
            plt.plot(history.history['loss'], label='loss')
            plt.plot(history.history['val_loss'], label='val_loss')
            plt.xlabel('Epoch')
            plt.ylabel('Accuracy')
            plt.legend(loc='upper right')
            plt.show()

            # Evaluating the model
            if loss_fun == 'sparse_categorical_crossentropy':
                test_loss, test_acc = model.evaluate(X_test_reshaped, Y_test, verbose=2)
            else:
                test_loss, test_acc = model.evaluate(X_test_reshaped, to_categorical(Y_test), verbose=2)

                # Displaying the results
            print("Loss: ", test_loss)
            print("Accuracy: ", test_acc)

            # calculate convergence
            initial_loss = history.history['loss'][0]
            final_loss = history.history['loss'][-1]
            convergence_length = len(history.history['loss']) - 1
            convergence_rate = abs(initial_loss - final_loss) / convergence_length
            print(convergence_rate)
            # Saving the scores
            optimizers.append(opt)
            loss_functions.append(loss_fun)
            loss_scores.append(test_loss)
            acc_scores.append(test_acc)
            converg_rates.append(convergence_rate)
            # Deleting the model obj
            del model

    results = pd.DataFrame()
    results["optimizer"] = optimizers
    results["Loss Functions"] = loss_functions
    results["Accuracy"] = acc_scores
    results["Loss"] = loss_scores
    results["rate"] = converg_rates

    print("\n\n ===============================================================================================\n")
    print(results)


if __name__ == '__main__':
    main()
