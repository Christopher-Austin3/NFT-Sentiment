import tensorflow as tf

import AICreation
import db
import AICreation as aic
import json


# get input data, normalise, call sentiment algorithm
def predict_sentiment(input_data):
    old_sentiments = db.read_sentiment()
    sentiment_avg = sum(old_sentiments) / len(old_sentiments)
    ai_params = get_params()
    predicted_sentiment = aic.forward_prop(input_data, ai_params)
    d_sentiment = linear_reg(sentiment_avg, predicted_sentiment)
    return d_sentiment


def get_params():
    counter = 0
    params = {}
    paramnames = ["W", "B"]
    with open("Parameters.npy", "rb") as f:
        for line in f:
            params[paramnames[counter % 2] + str((counter % 2) + 1)] = tf.Variable(line)
            counter += 1
    return params


# calculate sentiment as a function of input data [is_verified, followers, following]
def calculate_sentiment(input_data):
    return input_data[0] * (0.1 * input_data[1] + 0.005 * input_data[2] * 0.01 * input_data[3])


# returns change in sentiment
def linear_reg(old_sentiment, sentiment):
    return sentiment - old_sentiment
