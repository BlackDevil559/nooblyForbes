import http.client
import json

# Establishing a connection
conn = http.client.HTTPSConnection("reuters-business-and-financial-news.p.rapidapi.com")

# Headers with RapidAPI key
headers = {
    'x-rapidapi-key': "2ea2e9c90emsh023fc8de0ef582ep168d1fjsne981a8300d92",
    'x-rapidapi-host': "reuters-business-and-financial-news.p.rapidapi.com"
}

# Sending GET request to the specified endpoint
stock="Apple"
conn.request("GET", f"/get-articles-by-keyword-name/{stock}/0/20", headers=headers)

# Getting response from the server
res = conn.getresponse()
data = res.read()

# Decoding and formatting the response into JSON format
decoded_data = data.decode("utf-8")

try:
    # Load the data into a Python object
    json_data = json.loads(decoded_data)

    # Assuming articles are in a list format
    articles = json_data.get('articles', [])

    # Print only the article names (assuming 'articlesName' is a field in each article)
    for article in articles:
        print(article.get('articlesName'))
        print()

except json.JSONDecodeError:
    print("Failed to parse JSON data. Raw response:")
    print(decoded_data)
