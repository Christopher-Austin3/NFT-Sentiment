# Imported libraries
import datetime
from dateutil import parser
from functools import reduce
import json
import operator
import re
import requests
import sqlite3 as lite
import string
import threading
import time

# Functions

# Returns a dictionary including all API keys for the app
def getKeys(keyFilename):
    with open(keyFilename, "r") as myKeys:
        allKeys = json.loads(myKeys.read())
    return allKeys

# Adds the necessary OAuth authentication keys to a request
def addOAuth(req,auth):
    req.headers["Authorization"] = "Bearer " + auth
    req.headers["User-Agent"] = "v2FilteredStreamPython"
    return req

# Returns a lambda which produces the OAuth with a given key
def lambdaGenOAuth(auth):
    return lambda r: addOAuth(r, auth)

# Gets the current ruleset defined for the app's stream calls
def getRules(ruleUrl,authToken):
    res = requests.get(ruleUrl, auth=lambdaGenOAuth(authToken))
    return res.json()

# Deletes all pre-existing rules from the app
def deleteRules(ruleUrl, authToken, currRules):
    if currRules and "data" in currRules.keys():
        ids = list(map(lambda rule: rule["id"], currRules["data"]))
        payload = {"delete": {"ids": ids}}
        requests.post(ruleUrl, auth=lambdaGenOAuth(authToken), json=payload)

# Adds a given list of rules to the API endpoint's stored list
def setRules(ruleUrl, authToken, rulesList):
    payload = {"add": rulesList}
    requests.post(ruleUrl, auth=lambdaGenOAuth(authToken), json=payload)

# Given a list of rules, resets the API endpoint rules to those given
def resetRules(ruleUrl, authToken, rulesList):
    deleteRules(ruleUrl, authToken, getRules(ruleUrl, authToken))
    setRules(ruleUrl, authToken, rulesList)

# Given a list of required metadata tags, constructs an API request address
def constructRequest(streamUrl, tagsDict):
    base = streamUrl
    if len(tagsDict) == 0:
        return base
    else:
        base += "?"
        for key in tagsDict.keys():
            if type(tagsDict[key]) == str:
                base += key + "=" + tagsDict[key] + "&"
            else:
                base += key + "="
                for field in tagsDict[key]:
                    base += field + ","
                base = base[:-1] + "&"
        return base[:-1]

# Acquires a stream of Tweets given a request address
def stream(reqUrl, authToken, collectionSet, activeTweets):
    response = requests.get(reqUrl, auth=lambdaGenOAuth(authToken), stream=True)
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            tweetText = json_response["data"]["text"]
            mentioned = namedCollections(tweetText, collectionSet)
            if len(mentioned) != 0:
                activeTweets.append(json_response)
            # Stand-in for when we write the actually useful code
            print(namedCollections)

# Turns tweet text into a set of included words
def rawTweet(tweet):
    noPunctuation = tweet.translate(str.maketrans('', '', string.punctuation))
    split = set(map(lambda u: u.tolower() ,re.split(' \n\t', noPunctuation)))
    return split

# Get the set of collections named by a tweet
def namedCollections(tweet, collections):
    tweetWords = rawTweet(tweet)
    named = tweetWords.intersection(collections)
    return named

# Creates a thread to occasionally update the list of collections
def startCollectionUpdater(collectionSet, dbName):
    updater = threading.Thread(target= collectionUpdater, args= (collectionSet, 3600, dbName), daemon= True)
    updater.start()

# Gets the list of collections from the database and updates the one in memory
def collectionUpdater(collectionSet, waitTime, dbName):
    updateLock = threading.Lock()
    while True:
        con = lite.connect(dbName)
        cur = con.cursor()
        query = '''SELECT Collection FROM NFT'''
        cur.execute(query)
        # Locks the collection list whilst it updates it (passed by reference)
        with updateLock:
             collectionSet = collectionSet.union(set(cur.fetchall()))
        con.close()
        time.sleep(waitTime)

# Creates a thread to filter out old tweets and calculate the current sentiment value
def startSentimentCalculator(activeTweets, collectionSet, dbName, rate, tRange):
    calculator = threading.Thread(target= sentimentCalculator, args= (activeTweets, collectionSet, dbName, rate, tRange), daemon= True)
    calculator.start()

# Filters old tweets and calculates the current sentiment on each collection
def sentimentCalculator(activeTweets, collectionSet, dbName, rate, tRange):
    sentimentLock = threading.Lock()
    while True:
        with sentimentLock:
            activeTweets = filter(lambda t: timeCompare(t, tRange), activeTweets)
            activeTweets = map(lambda t: updateTweet(config["updateAddress"], t), activeTweets)
            relevantTweets = {}
            for collection in collectionSet:
                relevantTweets[collection] = filter(lambda t: collection in namedCollections(t, collectionSet), activeTweets)
                relevantTweets[collection] = map(getKeyData, relevantTweets[collection])
                relevantTweets[collection] = reduce(lambda d1,d2: map(operator.add, d1,d2), relevantTweets[collection])
        #TODO Invoke AI
        time.sleep(rate * 60)

# Get metrics for evaluation from a tweet
def getKeyData(tweet):
    authorId = tweet["data"]["author_id"]
    for possibleAuthor in tweet["includes"]["users"]:
        if possibleAuthor["id"] == authorId:
            author = possibleAuthor
    tweetDataList = [int(author["verified"]),
                     author["public_metrics"]["followers_count"],
                     author["public_metrics"]["following_count"],
                     author["public_metrics"]["tweet_count"]]
    #impressionsTotal = 0
    #for val in tweet["data"]["non_public_metrics"]:
    #    impressionsTotal += val
    #for val in tweet["data"]["public_metrics"]:
    #    impressionsTotal += val
    #tweetDataList.append(impressionsTotal)
    return tweetDataList

# Returns whether the tweet has been made within a certain time of the current time
def timeCompare(tweet, minutesRange):
    tweetTimeString = tweet["data"]["created_at"]
    datetimeMade = parser.parse(tweetTimeString)
    now = datetime.datetime.now().astimezone()
    timeDelta = now - datetimeMade
    return (minutesRange * 60) > timeDelta.seconds

# Gets the latest state value for a tweet
def updateTweet(updateUrl, tweet):
    tweetId = tweet["data"]["id"]
    allTags = config["tagsList"]
    allTags["ids"] = tweetId
    realUrl = constructRequest(updateUrl, tweet)
    res = requests.post(realUrl, auth=lambdaGenOAuth(keys["bearer"]))
    return json.loads(res)

# Main code
if __name__ == '__main__':
    # Getting config information
    with open("config.json", "r") as myConfig:
        config = json.loads(myConfig.read())

    # Getting API keys
    keys = getKeys(config["keyFile"])

    # Creating collection set and updater
    allCollections = {}
    startCollectionUpdater(allCollections, config["dbName"])

    # Setting the rules to the ones in the config
    resetRules(config["rulesAddress"], keys["bearer"], config["rulesList"])

    # Start the Tweet stream
    activeTweets = []
    stream(constructRequest(config["streamAddress"], config["tagsList"]), keys["bearer"], allCollections, activeTweets)
