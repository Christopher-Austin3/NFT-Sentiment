import json
import requests

# Functions
def getKeys(keyFilename):
    with open(keyFilename, "r") as myKeys:
        keys = json.loads(myKeys.read())
    return keys

def bearer_oauth(r):
    global allKeys
    token = allKeys["bearer"]
    r.headers["Authorization"] = "Bearer " + token
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r

def getRules():
    global allKeys
    response = requests.get("https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception("Cannot get rules (HTTP {}): {}".format(response.status_code, response.text))
    return response.json()

def deleteAllRules(rules):
    if rules is None or "data" not in rules:
        return None
    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post("https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth, json=payload)
    if response.status_code != 200:
        raise Exception("Cannot delete rules (HTTP {}): {}".format(response.status_code, response.text))

def setRules(rulesList):
    payload = {"add": rulesList}
    response = requests.post("https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth, json=payload,)
    if response.status_code != 201:
        raise Exception("Cannot add rules (HTTP {}): {}".format(response.status_code, response.text))

def constructRequest(tagsDict):
    base = "https://api.twitter.com/2/tweets/search/stream"
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

def stream(url):
    response = requests.get(url, auth=bearer_oauth, stream=True,)
    if response.status_code != 200:
        raise Exception("Cannot get stream (HTTP {}): {}".format(response.status_code, response.text))
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            print(json.dumps(json_response, indent=4, sort_keys=True))


# Main
if __name__ == '__main__':
    allKeys = getKeys("keys.json")
    newRules = [{"value": "nft has:images", "tag": "nft with images"}]
    tags = {"tweet.fields":["created_at","public_metrics","non_public_metrics"],
            "expansions":"author_id",
            "user.fields":["created_at","public_metrics"],
            }

    deleteAllRules(getRules())
    setRules(newRules)
    url = constructRequest(tags)
    stream(url)
