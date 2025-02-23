import os
from datetime import date
from bs4 import BeautifulSoup

import requests

url = "https://newsapi.org/v2/top-headlines"
api_key = os.environ['API_KEY']
sources = ["bbc-news", "cnn", "the-verge", "techcrunch", "espn", "medical-news-today"]

all_news = {source: {'titles': [], 'descriptions': [], 'urls': [], 'images': [], 'content': []} for source in sources}
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
    for i in range(len(data['articles'])):
        if source != "espn":
            all_news[source]['titles'].append(data['articles'][i]['title'].split("|")[0])
        else:
            all_news[source]['titles'].append(data['articles'][i]['title'].split("-")[0])
        all_news[source]['descriptions'].append(data['articles'][i]['description'])
        all_news[source]['urls'].append(data['articles'][i]['url'])
        all_news[source]['images'].append(data['articles'][i]['urlToImage'])
        all_news[source]['content'].append(data['articles'][i]['content'])

# for source in sources:
#     print(f"{source}: {all_news[source]['titles']}")
#     print(f"{source}: {all_news[source]['descriptions']}")
#     print(f"{source}: {all_news[source]['urls']}")
#     print(f"{source}: {all_news[source]['images']}")
#     print(f"{source}: {all_news[source]['content']}")
articel_content_urls = {source: [url for url in all_news[source]['urls']] for source in sources}
# print(articel_content_urls)

articel_content ={source:[] for source in sources}




for source in sources:
    for article_url in articel_content_urls[source]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        responses = requests.get(url=article_url,headers=headers)
        results=responses.text
        soup = BeautifulSoup(results, "html.parser")
        data_list = soup.select('p')
        single_string_data = ' '.join([item.get_text(strip=True) for item in data_list])
        articel_content[source].append(single_string_data)

for source in sources:
    print(articel_content[source])
