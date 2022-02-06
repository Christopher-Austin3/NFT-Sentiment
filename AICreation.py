import tensorflow as tf
from tensorflow import keras
import os
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def create_ai(x_train, y_train, x_test, y_test):
    x_train = normalise(slices_from_array(x_train))
    y_train = normalise(slices_from_array(y_train))
    x_test = normalise(slices_from_array(x_test))
    y_test = normalise(slices_from_array(y_test))
    params = initialise_parameters()
    # forward_prop(X, params)


def cost(A, y):
    return tf.reduce_mean(tf.keras.losses.binary_crossentropy(A, y))


# return Z4 not A4, calc lofits and reduce mean
def forward_prop(X, params):
    W1 = params['W1']
    B1 = params['B1']
    W2 = params['W2']
    B2 = params['B2']
    W3 = params['W3']
    B3 = params['B3']
    W4 = params['W4']
    B4 = params['B4']

    Z1 = tf.add(tf.matmul(W1, X), B1)
    A1 = tf.keras.activations.relu(Z1)
    Z2 = tf.add(tf.matmul(W2, A1), B2)
    A2 = tf.keras.activations.relu(Z2)
    Z3 = tf.add(tf.matmul(W3, A2), B3)
    A3 = tf.keras.activations.relu(Z3)
    Z4 = tf.add(tf.matmul(W4, A3), B4)
    # A4 = tf.keras.activations.relu(Z4)

    return Z4


def initialise_parameters():
    # W1: [5,5]
    # B1: [1, 5]
    # W2: [4, 5]
    # B2: [1, 4]
    # W3: [5, 4]
    # B3: [1, 5]
    # W4: [1, 5]
    # B4: [1, 1]
    initializer = tf.keras.initializers.GlorotNormal(seed=1)
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


def messtest():
    print(next(iter(slices_from_array([1, 2, 3, 4, 5, 6]))))


messtest()
