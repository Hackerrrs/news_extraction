from datetime import date

import requests

url = "https://newsapi.org/v2/top-headlines"
api_key = "0d2b941fac2844dcba7b9547be9d98bd"
sources = ["bbc-news", "cnn", "the-verge", "techcrunch", "espn", "medical-news-today"]
# categories = ["business", "entertainment", "health", "science", "sports", "technology"]
# all_news = {
#     "business": [],
#     "entertainment": [],
#     "health": [],
#     "science": [],
#     "sports": [],
#     "technology": []
# }

all_news = {source: [] for source in sources}
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
        if source!="espn":
            all_news[source].append(data['articles'][i]['title'].split("|")[0])
        else:
            all_news[source].append(data['articles'][i]['title'].split("-")[0])

for source in sources:
    print(f"{source}: {all_news[source]}")
