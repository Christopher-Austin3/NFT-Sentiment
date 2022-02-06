import tensorflow as tf;
import db
import AICreation as aic


# get input data, normalise, call sentiment algorithm
def predict_sentiment(input_data):
    normalised_input = aic.normalise(input_data)
    sentiment = calculate_sentiment(normalised_input)
    old_sentiment = db.read_sentiment()
    d_sentiment = linear_reg(old_sentiment, sentiment)
    db.write_sentiment(sentiment)




# use AI to calculate sentiment
def calculate_sentiment():
    return 0


# returns change in sentiment
def linear_reg(old_sentiment, sentiment):
    return 1.0
