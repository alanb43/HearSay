import tweepy
import requests
from config import TWITTER_BEARER_TOKEN, BING_API_KEY

class TweetSearcher:
    def __init__(self):
        self.client = tweepy.Client(TWITTER_BEARER_TOKEN)

    def get_tweets(self, query: str) -> list[str]:
        search_url = "https://api.bing.microsoft.com/v7.0/search"
        headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
        params = {"q": f"{query} site:twitter.com", "textDecorations": True, "textFormat": "HTML"}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        results = response.json()
        urls = [x['url'] for x in results['webPages']['value']]
        ids = []
        for url in urls:
            idx = url.find('status/')
            if idx != -1:
                ids.append(url[idx+7:])
        tweets = self.client.get_tweets(ids).data
        tweets = [tweet.text for tweet in tweets]
        return tweets
        