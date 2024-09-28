from fastapi import FastAPI, HTTPException
import requests
import json
import http.client
from transformers import pipeline

# Stock symbols mapping
stock_symbols = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Alphabet": "GOOGL",
    "Amazon": "AMZN",
    "Tesla": "TSLA",
    "Meta": "FB",
    "Netflix": "NFLX",
    "NVIDIA": "NVDA",
    "IBM": "IBM",
    "Oracle": "ORCL",
    "Intel": "INTC",
    "PayPal": "PYPL",
    "Cisco": "CSCO",
    "Salesforce": "CRM",
    "Reliance": "RELIANCE"
}

# Alpha Vantage News Class
class AlphaVantageNews:
    def __init__(self, stock, api_key):
        self.stock = stock_symbols.get(stock)
        self.api_key = api_key
        self.url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={self.stock}&apikey={self.api_key}'

    def get_news(self):
        try:
            r = requests.get(self.url)
            data = r.json()
            if 'feed' in data:
                return [f"{article.get('title', 'No title')} - {article.get('summary', 'No summary')}" for article in data['feed']]
            return ["No news available from AlphaVantage."]
        except Exception as e:
            return [f"Error fetching data from AlphaVantage: {e}"]

# CNBC News Class
class CNBCNews:
    def __init__(self, stock, api_key):
        self.stock = stock_symbols.get(stock)
        self.headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "cnbc.p.rapidapi.com"
        }
        self.url = "https://cnbc.p.rapidapi.com/news/v2/list-by-symbol"
        self.querystring = {"symbol": self.stock}

    def get_news(self):
        try:
            response = requests.get(self.url, headers=self.headers, params=self.querystring)
            data = response.json()
            if 'data' in data and 'symbolEntries' in data['data']:
                articles = data['data']['symbolEntries']['results']
                return [f"{article.get('headline', 'No headline')}" for article in articles]
            return ["No news available from CNBC."]
        except Exception as e:
            return [f"Error fetching data from CNBC: {e}"]

# Marketaux News Class
class MarketauxNews:
    def __init__(self, stock, api_key):
        self.stock = stock_symbols.get(stock)
        self.url = f"https://api.marketaux.com/v1/news/all?symbols={self.stock}&filter_entities=true&language=en&api_token={api_key}"

    def get_news(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                data = response.json()
                return [f"Source: Marketaux - News: {article.get('title', 'No title')} - {article.get('description', 'No description')}" for article in data.get("data", [])]
            return ["No news available from Marketaux."]
        except Exception as e:
            return [f"Error fetching data from Marketaux: {e}"]

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
                return [f"{article.get('title', 'No title')} - {article.get('url', 'No URL')}" for article in data['articles']]
            return ["No news available from NewsAPI."]
        except Exception as e:
            return [f"Error fetching data from NewsAPI: {e}"]

# Reuters News Class
class ReutersNews:
    def __init__(self, stock, api_key):
        self.stock = stock_symbols.get(stock)
        self.headers = {
            'x-rapidapi-key': api_key,
            'x-rapidapi-host': "reuters-business-and-financial-news.p.rapidapi.com"
        }
        self.conn = http.client.HTTPSConnection("reuters-business-and-financial-news.p.rapidapi.com")
        self.url = f"/get-articles-by-keyword-name/{self.stock}/0/20"

    def get_news(self):
        try:
            self.conn.request("GET", self.url, headers=self.headers)
            res = self.conn.getresponse()
            data = res.read()
            decoded_data = data.decode("utf-8")
            json_data = json.loads(decoded_data)
            articles = json_data.get('articles', [])
            if not articles:
                return ["No articles found for this stock."]
            return [f"{article.get('articlesName', 'No article name')}" for article in articles]
        except Exception as e:
            return [f"Error fetching news from Reuters: {e}"]

# API keys (replace with your actual keys)
api_keys = {
    'alphavantage': 'K8SCLOBSJSHO4OTJ',
    'cnbc': '2ea2e9c90emsh023fc8de0ef582ep168d1fjsne981a8300d92',
    'marketaux': 'U4E0cK4uKeLtv1KcnUZlwW3bwr5RuV8y8IVJAEzx',
    'newsapi': 'aadf548393194c0599a75ad3974c9513',
    'reuters': '78abf98e82msh71f5049b0b8b1adp1ce3c6jsn3d7f016c0d14'
}

# Initialize sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

# FastAPI app
app = FastAPI()

# Function to calculate the average sentiment score
def calculate_average_sentiment(news_list):
    total_score = 0
    count = 0

    for news in news_list:
        # Get the sentiment analysis result for each headline
        result = sentiment_pipeline(news)
        sentiment = result[0]['label']
        score = result[0]['score']

        # Adjust sentiment score based on label (positive = 1, negative = -1)
        if sentiment == 'NEGATIVE':
            score = -score

        total_score += score
        count += 1

    if count == 0:
        return 0  # Avoid division by zero

    return total_score / count

@app.get("/get-news")
def get_stock_news(stock: str):
    if stock not in stock_symbols:
        raise HTTPException(status_code=400, detail="Stock symbol not supported.")

    alphavantage_news = AlphaVantageNews(stock, api_keys['alphavantage']).get_news()
    cnbc_news = CNBCNews(stock, api_keys['cnbc']).get_news()
    marketaux_news = MarketauxNews(stock, api_keys['marketaux']).get_news()
    newsapi_news = NewsAPI(stock, api_keys['newsapi']).get_news()
    reuters_news = ReutersNews(stock, api_keys['reuters']).get_news()

    # Combine all news sources into one dictionary
    all_news = {
        "AlphaVantage": alphavantage_news,
        "CNBC": cnbc_news,
        "Marketaux": marketaux_news,
        "NewsAPI": newsapi_news,
        "Reuters": reuters_news
    }

    # Add sentiment analysis results
    sentiment_results = {}
    for source, news_list in all_news.items():
        if isinstance(news_list, list) and news_list and "Error" not in news_list[0]:
            avg_sentiment = calculate_average_sentiment(news_list)
            sentiment_results[source] = {
                "news": news_list,
                "average_sentiment": avg_sentiment
            }
        else:
            sentiment_results[source] = {
                "news": news_list,
                "average_sentiment": None
            }

    return sentiment_results

# To run the API using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
