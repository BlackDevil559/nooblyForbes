import requests
import json

# Your API token
api_token = "U4E0cK4uKeLtv1KcnUZlwW3bwr5RuV8y8IVJAEzx"
stock ="AAPL"
# API endpoint URL
url = f"https://api.marketaux.com/v1/news/all?symbols={stock}&filter_entities=true&language=en&api_token=" + api_token

# Send GET request to the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON data from the response
    data = response.json()
    # Loop through the data and extract titles and descriptions
    for article in data.get("data", []):
        title = article.get("title", "No title")
        description = article.get("description", "No description")
        print(f"Title: {title}")
        print(f"Description: {description}")
        print("-" * 80)
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
