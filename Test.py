import requests
print("hello world")

url = "https://api.opensea.io/api/v1/assets?order_direction=desc&offset=0&limit=20"

headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers)

print(response.text)