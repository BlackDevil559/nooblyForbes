# This returns a pandas DataFrame and saves it to data/data.csv by default (see options)

from stocknews import StockNews
...
stocks = ['AAPL']
sn = StockNews(stocks, wt_key='MY_WORLD_TRADING_DATA_KEY')
df = sn.summarize()


# stocks: A list of stocks to check. See http://eoddata.com/symbols.aspx for all symbols available
# news_file='news.csv': filename of the saved news
# summary_file='data.csv': filename of the saved dataset, including sentiment and value per day and stock
# save_news=True: save the news file or scrape and analyse on the fly for recent news
# closing_hour=20: Close of the exchange (NASDAQ in this case). News after closing will be taken for next trading day (skips the weekend as well)
# closing_minute=0: Same as closing_hour
# wt_key=None: Your worldtradingdata.com API Key. Get one here. Not needed if read_rss is called directly.