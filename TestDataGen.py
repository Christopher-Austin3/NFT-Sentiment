import requests
import json
import sqlite3 as lite
import re
import string
import datetime
from dateutil import parser

def addOAuth(req,auth):
    req.headers["Authorization"] = "Bearer " + auth
    req.headers["User-Agent"] = "v2FilteredStreamPython"
    return req

# Turns tweet text into a set of included words
def rawTweet(tweet):
    noPunctuation = tweet.translate(str.maketrans('', '', string.punctuation))
    split = set(map(lambda u: u.lower(), re.split(' |\n|\t', noPunctuation)))
    return split

# Get the set of collections named by a tweet
def namedCollections(tweet, collections):
    tweetWords = rawTweet(tweet)
    named = tweetWords.intersection(collections)
    return named

if __name__ == '__main__':
    url = "https://api.twitter.com/2/tweets/search/recent?query=\"nft\"" \
          "&tweet.fields=created_at" \
          "&expansions=author_id" \
          "&user.fields=created_at,public_metrics,verified" \
          "&max_results=100"

    extra = ""

    with open("keys.json","r") as myFile:
        keys = json.loads(myFile.read())
    bearerKey = keys["bearer"]

    con = lite.connect("nftDatabase.db")
    cur = con.cursor()
    query = '''SELECT Collection FROM NFT'''
    cur.execute(query)
    collections = cur.fetchall()
    allCollections = set()
    for col in collections:
        allCollections.add(col[0])
    con.close()
    print(allCollections)

    nextToken = ""

    goodTweet = []
    while nextToken is not None:
        res = requests.get(url+extra, auth= lambda r: addOAuth(r, bearerKey))
        allRes = res.json()
        print(allRes)
        if "title" in allRes.keys() and "Too Many Requests" in allRes.values():
            nextToken = None
        else:
            allData = res.json()["data"]
            nextToken = allRes["meta"]["next_token"]
            for tweet in allData:
                named = namedCollections(tweet["text"], allCollections)
                if len(named) != 0:
                    # The tweet is relevant to our training collections
                    authorId = tweet["author_id"]
                    for potential in allRes["includes"]["users"]:
                        if potential["id"] == authorId:
                            author = potential
                    goodTweet.append((tweet,author))
            print(len(goodTweet))
            latestTweet = goodTweet[-1][0]
            timeMade = parser.parse(latestTweet["created_at"])
            now = datetime.datetime.now().astimezone()
            timeDelta = now - timeMade
            print(timeDelta.seconds)
            if timeDelta.seconds > (60*60):
                nextToken = None
            extra = "&next_token=" + nextToken

    # Splitting into groups for testing
    timeBatches = []
    lastUpdate = datetime.datetime.now().astimezone()
    thisBatch = []
    for tweet in goodTweet:
        thisBatch.append(tweet)
        timeMade = parser.parse(tweet[0]["created_at"])
        timeDelta = lastUpdate - timeMade
        if timeDelta.seconds > 600:
            timeBatches.append(thisBatch)
            thisBatch = []
            lastUpdate = timeMade
    timeBatches.append(thisBatch)

    # For each group create dictionary
    allDicts = []
    for batch in timeBatches:
        newD = {"total":len(batch)}
        for col in allCollections:
            initialScores = [0,0,0,0]
            for tweet in batch:
                if col in namedCollections(tweet[0]["text"],allCollections):
                    initialScores[0] += int(tweet[1]["verified"])
                    initialScores[1] += tweet[1]["public_metrics"]["followers_count"]
                    initialScores[2] += tweet[1]["public_metrics"]["following_count"]
                    initialScores[3] += tweet[1]["public_metrics"]["tweet_count"]
            newD[col] = initialScores
        allDicts.append(newD)

    with open("testData.json","w") as myFile:
        myFile.write(json.dumps(allDicts))
