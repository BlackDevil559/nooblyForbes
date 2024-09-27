import http.client
import json

conn = http.client.HTTPSConnection("twitter-api45.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "2ea2e9c90emsh023fc8de0ef582ep168d1fjsne981a8300d92",
    'x-rapidapi-host': "twitter-api45.p.rapidapi.com"
}
conn.request("GET", "/usermedia.php?screenname=FederalReserve", headers=headers)
res = conn.getresponse()
data = res.read()
response_text = data.decode("utf-8")
tweets_data = json.loads(response_text)
if "timeline" in tweets_data:
    for tweet in tweets_data["timeline"]:
        tweet_text = tweet.get("text", "")
        print(f"Tweet ID: {tweet['tweet_id']}")
        print(f"Text: {tweet_text}")
        print(f"Favorites: {tweet['favorites']}")
        print(f"Retweets: {tweet.get('retweets', 0)}")
        print(f"Created At: {tweet['created_at']}")
        print(f"Views: {tweet.get('views', 'N/A')}")
        print("-" * 50)
else:
    print("No tweets found or error in response.")
