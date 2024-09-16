import requests
stock ="AMZN"
url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={stock}&apikey=K8SCLOBSJSHO4OTJ'
r = requests.get(url)
data = r.json()

# Extract summaries from the news articles
if 'feed' in data:
    for article in data['feed']:
        print(f"Title: {article['title']}")
        print(f"Summary: {article['summary']}")
        print("-" * 50)
else:
    print("No news feed found")
