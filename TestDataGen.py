import requests
import json

def addOAuth(req,auth):
    req.headers["Authorization"] = "Bearer " + auth
    req.headers["User-Agent"] = "v2FilteredStreamPython"
    return req

if __name__ == '__main__':
    url = "https://api.twitter.com/2/tweets/search/recent?query=\"nft\"" \
          "&tweet.fields=created_at" \
          "&expansions=author_id" \
          "&user.fields=created_at,public_metrics,verified" \
          "&max_results=100"

    with open("keys.json","r") as myFile:
        keys = json.loads(myFile.read())
    bearerKey = keys["bearer"]

    res = requests.get(url, auth= lambda r: addOAuth(r, bearerKey))
    print(json.dumps(res.json(), indent=4, sort_keys=True))
