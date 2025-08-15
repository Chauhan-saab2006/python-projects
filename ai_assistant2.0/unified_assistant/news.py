import requests

NEWS_API_KEY = 'b3453c25bd244728bf3c54bc3682d13f'  # Replace with your NewsAPI key


def get_top_headlines(category='technology', country='us', page_size=10):
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': country,
        'category': category,
        'pageSize': page_size,
        'apiKey': NEWS_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return [
            {
                'title': article['title'],
                'source': article['source']['name'],
                'url': article['url']
            }
            for article in data.get('articles', [])
        ]
    else:
        return [{'error': f'Error: {response.status_code}', 'details': response.text}]
