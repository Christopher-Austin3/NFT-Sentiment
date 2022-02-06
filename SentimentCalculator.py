import tensorflow as tf;
import db
import AICreation as aic


# get input data, normalise, call sentiment algorithm
def predict_sentiment(input_data):
    current_sentiment = calculate_sentiment(input_data)
    old_sentiments = db.read_sentiment()
    d_sentiment = linear_reg(old_sentiments, current_sentiment)
    db.write_sentiment(current_sentiment)


# calculate sentiment as a function of input data
def calculate_sentiment(input_data):
    return


# returns change in sentiment
def linear_reg(old_sentiment, sentiment):
    return 1.0
