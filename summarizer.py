from utils import query, FINE_TUNED

API_URL = "https://api-inference.huggingface.co/models/knkarthick/MEETING_SUMMARY"
if FINE_TUNED:
    from transformers import pipeline

class Summarizer:
    def __init__(self):
        if FINE_TUNED:
            self.model = pipeline("summarization", model="knkarthick/MEETING_SUMMARY")

    def summarize_tweets(self, tweets):
        print("summarizing tweets")
        tweets_paragraph = ' '.join(tweets)
        if FINE_TUNED:
            return self.model(tweets_paragraph, truncation=True)
        
        return query(tweets_paragraph, API_URL)

    def _combine_tweets(self, tweets):
        tweets_paragraph = ""
        for tweet in tweets:
            tweets_paragraph += tweet["content"] + " "
        
        return tweets_paragraph


