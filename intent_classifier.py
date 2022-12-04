from utils import query, FINE_TUNED
from data_classes.intents import INTENTS

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
if FINE_TUNED:
    from transformers import pipeline

class IntentClassifier:
    """Classifies Intent"""

    def __init__(self):
        if FINE_TUNED:
            self.clf = pipeline(
                task='zero-shot-classification', 
                model='facebook/bart-large-mnli',
                multi_label=True
            )

    def classify_intent(self, text):
        print("classifying intent")
        if FINE_TUNED:
            return self.clf(text, INTENTS)

        payload = {
            "inputs": text,
            "parameters": {"candidate_labels": INTENTS},
        }

        return query(payload, API_URL)
