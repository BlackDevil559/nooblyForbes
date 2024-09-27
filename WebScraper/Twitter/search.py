import http.client
import json

conn = http.client.HTTPSConnection("twitter293.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "2ea2e9c90emsh023fc8de0ef582ep168d1fjsne981a8300d92",
    'x-rapidapi-host': "twitter293.p.rapidapi.com"
}

conn.request("GET", "/search/Google?count=5&category=Latest&filters=%7B%22since%22%3A+%222020-10-01%22%7D", headers=headers)

res = conn.getresponse()
data = res.read()

response_text = data.decode("utf-8")

tweets_data = json.loads(response_text)
print(tweets_data)
