import tensorflow as tf
from tensorflow import keras
# import numpy as np
import matplotlib.pyplot as plt


def create_ai(x_train, y_train, x_test, y_test):
    x_train = normalise(slices_from_array(x_train))
    y_train = normalise(slices_from_array(y_train))
    x_test = normalise(slices_from_array(x_test))
    y_test = normalise(slices_from_array(y_test))
    # params = initialise_parameters()
    # forward_prop(X, params)


def learn(x_train, y_train, x_test, y_test, learning_rate=0.001,
          epochs=500, minibatch_size=8):
    params = initialise_parameters()
    x_train_batch = x_train.batch(minibatch_size)
    y_train_batch = y_train.batch(minibatch_size)
    (W1, B1, W2, B2, W3, B3, W4, B4) = getparams(params)
    sgd = keras.optimizers.SGD(learning_rate)
    all_costs = []

    for epoch in range(epochs):
        intermediary_cost = 0
        for (x_minibatch, y_minibatch) in (x_train_batch, y_train_batch):
            with tf.GradientTape() as t:
                activation = forward_prop(x_minibatch, params)
                network_cost = cost(activation, y_minibatch)
            gradient_changes = t.gradient(network_cost, [W1, B1, W2, B2, W3, B3, W4, B4])
            sgd.apply_gradients(zip(gradient_changes, [W1, B1, W2, B2, W3, B3, W4, B4]))
            intermediary_cost += network_cost
        all_costs.append(intermediary_cost)

    plt.plot(all_costs)
    plt.xlabel("epochs")
    plt.ylabel("cost")
    plt.show()

    return params


def cost(A, y):
    return tf.reduce_mean(keras.losses.binary_crossentropy(A, y))


def getparams(params):
    return (params['W1'], params['B1'], params['W2'], params['B2'],
            params['W3'], params['B3'], params['W4'], params['B4'])


# return Z4 not A4, calc lofits and reduce mean
def forward_prop(X, params):
    (W1, B1, W2, B2, W3, B3, W4, B4) = getparams(params)

    Z1 = tf.add(tf.matmul(W1, X), B1)
    A1 = keras.activations.relu(Z1)
    Z2 = tf.add(tf.matmul(W2, A1), B2)
    A2 = keras.activations.relu(Z2)
    Z3 = tf.add(tf.matmul(W3, A2), B3)
    A3 = keras.activations.relu(Z3)
    Z4 = tf.add(tf.matmul(W4, A3), B4)
    A4 = keras.activations.relu(Z4)

    return A4


def initialise_parameters():
    # W1: [5,5]
    # B1: [1, 5]
    # W2: [4, 5]
    # B2: [1, 4]
    # W3: [5, 4]
    # B3: [1, 5]
    # W4: [1, 5]
    # B4: [1, 1]
    initializer = keras.initializers.GlorotNormal(seed=1)
    W1 = tf.Variable(initializer(shape=(5, 5)))
    B1 = tf.Variable(initializer(shape=(1, 5)))
    W2 = tf.Variable(initializer(shape=(4, 5)))
    B2 = tf.Variable(initializer(shape=(1, 4)))
    W3 = tf.Variable(initializer(shape=(5, 4)))
    B3 = tf.Variable(initializer(shape=(1, 5)))
    W4 = tf.Variable(initializer(shape=(1, 5)))
    B4 = tf.Variable(initializer(shape=(1, 1)))

    weights_and_biases = {"W1": W1, "B1": B1, "W2": W2, "B2": B2,
                          "W3": W3, "B3": B3, "W4": W4, "B4": B4}
    return weights_and_biases


def slices_from_array(array):
    const = tf.constant(array)
    return tf.data.Dataset.from_tensor_slices(const)


# normalise input data
def normalise(data):
    # tf cast, reshape
    return data


