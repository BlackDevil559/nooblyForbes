import requests

# Define the URL and parameters
url = "https://cnbc.p.rapidapi.com/news/v2/list-by-symbol"
querystring = {"page": "1", "pageSize": "30", "symbol": "AAPL"}

# Define the headers
headers = {
    "x-rapidapi-key": "2ea2e9c90emsh023fc8de0ef582ep168d1fjsne981a8300d92",
    "x-rapidapi-host": "cnbc.p.rapidapi.com"
}

# Send the GET request
response = requests.get(url, headers=headers, params=querystring)

# Parse the JSON response
data = response.json()

# Check if 'symbolEntries' and 'results' exist
if 'data' in data and 'symbolEntries' in data['data']:
    articles = data['data']['symbolEntries']['results']
    
    # Extract and print the headlines
    for article in articles:
        if 'headline' in article:
            print(article['headline'])
else:
    print("No data available")
