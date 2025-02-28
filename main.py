import os
from datetime import date
from bs4 import BeautifulSoup
import requests

def fetch_and_organize_news():
    url = "https://newsapi.org/v2/top-headlines"
    api_key = 'API_KEY'
    sources = ["bbc-news", "cnn", "the-verge", "techcrunch", "espn", "medical-news-today"]

    organized_news = []

    for source in sources:
        params = {
            "sources": source,
            "from": date.today().isoformat(),
            "sortBy": "popularity",
            "apiKey": api_key,
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.get(url=url, params=params, headers=headers)
        data = response.json()

        source_articles = []
        
        for i in range(len(data['articles'])):
            article_data = {
                "title": data['articles'][i]['title'].split("|")[0] if source != "espn" else data['articles'][i]['title'].split("-")[0],
                "description": data['articles'][i]['description'],
                "url": data['articles'][i]['url'],
                "image": data['articles'][i]['urlToImage'],
                "content": data['articles'][i]['content']
            }
            source_articles.append(article_data)

        for article in source_articles:
            article_url = article['url']
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            try:
                response = requests.get(url=article_url, headers=headers, timeout=5)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                data_list = soup.select('p')
                full_content = ' '.join([item.get_text(strip=True) for item in data_list])
                article['full_content'] = full_content
            except requests.RequestException as e:
                print(f"Error fetching content from {article_url}: {e}")
                article['full_content'] = "Content not available"

        organized_news.append(source_articles)

    return organized_news

news_data = fetch_and_organize_news()
for source_articles in news_data:
    for article in source_articles:
        print(article)
