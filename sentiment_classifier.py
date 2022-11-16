from transformers import pipeline

MODEL_DIR = 'sentiment-analysis/finetune-sentiment-model-players-teams/checkpoint-2'

class SentimentClassifier:
    "Analyzes text and returns positive, neutral, and negative"

    def __init__(self):
        self.sentiment = pipeline(
            task='sentiment-analysis',
            model=MODEL_DIR,
            tokenizer=MODEL_DIR,
        )

    def analyze(self, text):
        return self.sentiment(text)