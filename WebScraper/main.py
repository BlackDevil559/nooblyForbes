import requests
import json
import http.client
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
                return [f"Source: AlphaVantage - News: {article.get('title', 'No title')} - {article.get('summary', 'No summary')}" for article in data['feed']]
            return ["No news available from AlphaVantage."]
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
                articles = data['data']['symbolEntries']['results']
                return [f"Source: CNBC - News: {article.get('headline', 'No headline')}" for article in articles]
            return ["No news available from CNBC."]
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
                return [f"Source: Finnhub - News: {article.get('headline', 'No headline')} - {article.get('url', 'No URL')}" for article in data]
            return ["No news available from Finnhub."]
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
                return [f"Source: Marketaux - News: {article.get('title', 'No title')} - {article.get('description', 'No description')}" for article in data.get("data", [])]
            return ["No news available from Marketaux."]
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
                return [f"Source: NewsAPI - News: {article.get('title', 'No title')} - {article.get('url', 'No URL')}" for article in data['articles']]
            return ["No news available from NewsAPI."]
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
            return [f"Source: Seeking Alpha - News: {article.get('title', 'No title')} - {article.get('summary', 'No summary')}" for article in data.get('data', [])]
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
        self.conn = http.client.HTTPSConnection("reuters-business-and-financial-news.p.rapidapi.com")
        self.url = f"/get-articles-by-keyword-name/{self.stock}/0/20"

    def get_news(self):
        try:
            # Sending the GET request
            self.conn.request("GET", self.url, headers=self.headers)
            
            # Getting the response
            res = self.conn.getresponse()
            data = res.read()
            
            # Decoding the response
            decoded_data = data.decode("utf-8")
            
            # Parsing the JSON data
            json_data = json.loads(decoded_data)
            
            # Extracting articles and handling empty response
            articles = json_data.get('articles', [])
            if not articles:
                return ["No articles found for this stock."]

            # Formatting the articles
            return [f"Source: Reuters - News: {article.get('articlesName', 'No article name')}" for article in articles]
        
        except json.JSONDecodeError:
            print("Failed to parse JSON data. Raw response:")
            print(decoded_data)
            return ["Error parsing the data."]
        
        except Exception as e:
            print(f"Error fetching data from Reuters: {e}")
            return [f"Error fetching news: {e}"]

# Main Code to Run News Collection Individually
if __name__ == "__main__":
    stock_name = 'Apple'  # Change to the required stock symbol
    api_keys = {
        'alphavantage': 'K8SCLOBSJSHO4OTJ',
        'cnbc': '2ea2e9c90emsh023fc8de0ef582ep168d1fjsne981a8300d92',
        'finnhub': 'crjtc51r01qnnbrt3h8gcrjtc51r01qnnbrt3h90',
        'marketaux': 'U4E0cK4uKeLtv1KcnUZlwW3bwr5RuV8y8IVJAEzx',
        'newsapi': 'aadf548393194c0599a75ad3974c9513',
        'seekingalpha': '2ea2e9c90emsh023fc8de0ef582ep168d1fjsne981a8300d92',
        'reuters': '2ea2e9c90emsh023fc8de0ef582ep168d1fjsne981a8300d92'
    }

    # Fetching news from individual sources
    alphavantage_news = AlphaVantageNews(stock_name, api_keys['alphavantage']).get_news()
    cnbc_news = CNBCNews(stock_name, api_keys['cnbc']).get_news()
    # finnhub_news = FinnhubNews(stock_name, api_keys['finnhub']).get_news()
    marketaux_news = MarketauxNews(stock_name, api_keys['marketaux']).get_news()
    newsapi_news = NewsAPI(stock_name, api_keys['newsapi']).get_news()
    seekingalpha_news = SeekingAlphaNews(stock_name, api_keys['seekingalpha']).get_news()
    reuters_news = ReutersNews(stock_name, api_keys['reuters']).get_news()

    # Print results from each source
    all_news = reuters_news
    for news in all_news:
        print(news)
