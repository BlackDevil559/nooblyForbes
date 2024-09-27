from newsapi import NewsApiClient
from datetime import date, timedelta

phrase = "Apple"
newsapi = NewsApiClient(api_key="aadf548393194c0599a75ad3974c9513")
my_date = date.today() - timedelta(days = 7)
articles = newsapi.get_everything(q=phrase,
                                  from_param = my_date.isoformat(),
                                  language="en",
                                  sort_by="relevancy",
                                  page_size = 5)
for article in articles['articles']:
  print(article['title']+ ' | ' + article['publishedAt'] + ' | ' + article['url'])