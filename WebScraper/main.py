import requests
import json

# Alpha Vantage News Class
class AlphaVantageNews:
    def __init__(self, stock, api_key):
        self.stock = stock
        self.api_key = api_key
        self.url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={self.stock}&apikey={self.api_key}'

    def get_news(self):
        try:
            r = requests.get(self.url)
            data = r.json()
            if 'feed' in data:
                return [(article['title'], article['summary']) for article in data['feed']]
            else:
                return []
        except Exception as e:
            print(f"Error fetching data from AlphaVantage: {e}")
            return []

# CNBC News Class
class CNBCNews:
    def __init__(self, stock, api_key):
        self.stock = stock
        self.headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "cnbc.p.rapidapi.com"
        }
        self.url = "https://cnbc.p.rapidapi.com/news/v2/list-by-symbol"
        self.querystring = {"page": "1", "pageSize": "30", "symbol": stock}

    def get_news(self):
        try:
            response = requests.get(self.url, headers=self.headers, params=self.querystring)
            data = response.json()
            if 'data' in data and 'symbolEntries' in data['data']:
                return [(article.get('headline'), article.get('url')) for article in data['data']['symbolEntries']['results']]
            else:
                return []
        except Exception as e:
            print(f"Error fetching data from CNBC: {e}")
            return []

# Finnhub News Class
class FinnhubNews:
    def __init__(self, stock, api_key):
        self.stock = stock
        self.url = f"https://finnhub.io/api/v1/company-news?symbol={self.stock}&from=2023-08-15&to=2023-08-20&token={api_key}"

    def get_news(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                data = response.json()
                return [(article.get('headline'), article.get('url')) for article in data]
            return []
        except Exception as e:
            print(f"Error fetching data from Finnhub: {e}")
            return []

# Marketaux News Class
class MarketauxNews:
    def __init__(self, stock, api_key):
        self.stock = stock
        self.url = f"https://api.marketaux.com/v1/news/all?symbols={stock}&filter_entities=true&language=en&api_token={api_key}"

    def get_news(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                data = response.json()
                return [(article.get("title", "No title"), article.get("description", "No description")) for article in data.get("data", [])]
            return []
        except Exception as e:
            print(f"Error fetching data from Marketaux: {e}")
            return []

# NewsAPI Class
class NewsAPI:
    def __init__(self, stock, api_key):
        self.phrase = f"{stock} stock"
        self.api_key = api_key
        self.url = "https://newsapi.org/v2/everything"

    def get_news(self):
        try:
            querystring = {
                "q": self.phrase,
                "language": "en",
                "sortBy": "relevancy",
                "apiKey": self.api_key
            }
            response = requests.get(self.url, params=querystring)
            data = response.json()
            if 'articles' in data:
                return [(article['title'], article['url']) for article in data['articles']]
            return []
        except Exception as e:
            print(f"Error fetching data from NewsAPI: {e}")
            return []

# Seeking Alpha News Class
class SeekingAlphaNews:
    def __init__(self, stock, api_key):
        self.stock = stock
        self.headers = {
            'x-rapidapi-key': api_key,
            'x-rapidapi-host': "seeking-alpha.p.rapidapi.com"
        }
        self.url = f"https://seeking-alpha.p.rapidapi.com/news/v2/list-by-symbol?size=20&number=1&id={self.stock}"

    def get_news(self):
        try:
            conn = requests.get(self.url, headers=self.headers)
            data = conn.json()
            return [(article.get('title', "No title"), article.get('summary', "No summary")) for article in data.get('data', [])]
        except Exception as e:
            print(f"Error fetching data from Seeking Alpha: {e}")
            return []

# Reuters News Class
class ReutersNews:
    def __init__(self, stock, api_key):
        self.stock = stock
        self.headers = {
            'x-rapidapi-key': api_key,
            'x-rapidapi-host': "reuters-business-and-financial-news.p.rapidapi.com"
        }
        self.url = f"https://reuters-business-and-financial-news.p.rapidapi.com/get-articles-by-keyword-name/{self.stock}/0/20"

    def get_news(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            data = response.json()
            return [(article.get('title', "No title"), article.get('url', "No URL")) for article in data.get('articles', [])]
        except Exception as e:
            print(f"Error fetching data from Reuters: {e}")
            return []

# StockNews Aggregator Class
class StockNewsAggregator:
    def __init__(self, stock, api_keys):
        self.stock = stock
        self.api_keys = api_keys
        self.sources = [
            AlphaVantageNews(stock, api_keys['alphavantage']),
            CNBCNews(stock, api_keys['cnbc']),
            FinnhubNews(stock, api_keys['finnhub']),
            MarketauxNews(stock, api_keys['marketaux']),
            NewsAPI(stock, api_keys['newsapi']),
            SeekingAlphaNews(stock, api_keys['seekingalpha']),
            ReutersNews(stock, api_keys['reuters'])
        ]

    def fetch_all_news(self):
        all_news = []
        for source in self.sources:
            news = source.get_news()
            if news:
                all_news.extend(news)
        return all_news if all_news else ["No news available for this stock."]

# Main Code to Run Aggregator
if __name__ == "__main__":
    stock_name = 'AAPL'  # Change to the required stock symbol
    api_keys = {
        'alphavantage': 'K8SCLOBSJSHO4OTJ',
        'cnbc': '2ea2e9c90emsh023fc8de0ef582ep168d1fjsne981a8300d92',
        'finnhub': 'crjtc51r01qnnbrt3h8gcrjtc51r01qnnbrt3h90',
        'marketaux': 'U4E0cK4uKeLtv1KcnUZlwW3bwr5RuV8y8IVJAEzx',
        'newsapi': 'aadf548393194c0599a75ad3974c9513',
        'seekingalpha': '2ea2e9c90emsh023fc8de0ef582ep168d1fjsne981a8300d92',
        'reuters': '2ea2e9c90emsh023fc8de0ef582ep168d1fjsne981a8300d92'
    }

    aggregator = StockNewsAggregator(stock_name, api_keys)
    news = aggregator.fetch_all_news()

    for title, summary in news:
        print(f"Title: {title}")
        print(f"Summary: {summary}")
        print("-" * 80)
