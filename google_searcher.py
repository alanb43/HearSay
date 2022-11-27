import tweepy
from googlesearch import search
from config import TWITTER_BEARER_TOKEN

class GoogleSearcher:
    def __init__(self):
        self.client = tweepy.Client(TWITTER_BEARER_TOKEN)

    def get_tweets(self, query: str) -> list[str]:
        results = search(f"{query} site:twitter.com", num_results=10)
        ids = []
        for result in results:
            idx = result.find('status/')
            if idx != -1:
                ids.append(result[idx+7:])
        return [self.client.get_tweet(id) for id in ids]
        