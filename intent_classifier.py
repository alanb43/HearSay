from transformers import pipeline

class IntentClassifier:
    """Classifies Intent"""

    def __init__(self, labels_in):
        self.clf = pipeline('zero-shot-classification', model='facebook/bart-large-mnli', multi_label=True)
        self.labels = labels_in

    def classify_intent(self, text) -> str:
        return self.clf(text, self.labels)