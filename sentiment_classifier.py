from transformers import pipeline

class SentimentClassifier:
    "Analyzes text and returns positive, neutral, and negative"

    def __init__(self):
        self.sentiment = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")

    def analyze(self, text):
        return self.sentiment(text)