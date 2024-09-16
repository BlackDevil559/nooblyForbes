import requests
from bs4 import BeautifulSoup
url = "https://www.moneycontrol.com/news/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

news_section = soup.find('section', class_='startup-news section')

# Iterate through each news item and extract the headlines
news_headlines = []
for news_item in news_section.find_all('h3', class_='related_des'):
    headline = news_item.text.strip()
    news_headlines.append(headline)

# Print the extracted headlines
for i, headline in enumerate(news_headlines, start=1):
    print(f"{i}. {headline}")

data = {'Date': ['2024-08-28'],
        'Headlines': news_headlines}
