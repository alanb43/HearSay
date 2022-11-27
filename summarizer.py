from transformers import pipeline

class Summarizer:

    def __init__(self):
        self.model = pipeline("summarization", model="knkarthick/MEETING_SUMMARY")

    def summarize_tweets(self, tweets):
        tweets_paragraph = self._combine_tweets(tweets)
        #print("TWEETS PARAGRAPH \n\n", tweets_paragraph)
        return self.model(tweets_paragraph, truncation=True)
        
    def _combine_tweets(self, tweets):
        tweets_paragraph = ""
        for tweet in tweets:
            tweets_paragraph += tweet["content"] + " "
        return tweets_paragraph


