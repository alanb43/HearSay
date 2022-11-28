from transformers import pipeline
from data_classes.sentiment import Sentiment
from random import randrange

# Switch between the two if model doesn't work
# MODEL_DIR = 'sentiment-analysis/finetune-sentiment-model-players-teams'
MODEL_DIR = 'cardiffnlp/twitter-roberta-base-sentiment-latest'

class SentimentClassifier:
    """
    Derives positive, negative, or neutral sentiment from language.
    Model fine-tuned on soccer and basketball tweets for different players.
    """

    def __init__(self):
        self._analyze_pipeline = pipeline(
            task='sentiment-analysis',
            model=MODEL_DIR,
            tokenizer=MODEL_DIR,
        )

    def analyze(self, text: str):
        """Returns sentiment and confidence for given text input."""
        analysis = self._analyze_pipeline(text)[0]
        return {"sentiment": analysis["label"], "confidence": analysis["score"]}

    def batch_analysis(self, tweets: list):
        """
        Derives an overall sentiment for the batch of tweets.
        Should be ran on a generally large pool of tweets, uses only high 
            confidence datapoints to draw conclusions.
        """

        # this line doesn't make each object a pointer to each other
        positive_count = neutral_count = negative_count = 0
        positive_batch = [] # doing it
        neutral_batch = []  # for these
        negative_batch = [] # would however

        for tweet in tweets:
            analysis = self.analyze(tweet)
            sentiment, confidence = analysis["sentiment"], analysis["confidence"]
            if confidence > 0.75:
                if sentiment == Sentiment.POSITIVE:
                    positive_count += 1
                    positive_batch.append(tweet)
                elif sentiment == Sentiment.NEUTRAL:
                    neutral_count += 1
                    neutral_batch.append(tweet)
                else:
                    negative_count += 1
                    negative_batch.append(tweet)
        positive_conf = self._calculate_batch_confidence(positive_count,
                                                         negative_count)
        neutral_conf = self._calculate_batch_confidence(neutral_count,
                                                        positive_count,
                                                        negative_count)
        negative_conf = self._calculate_batch_confidence(negative_count,
                                                         positive_count)

        best_result = max(positive_conf, neutral_conf, negative_conf)
        if best_result < 0.50:
            return "Sentiment could not be derived reliably"
        
        data = {"sentiment": "", "confidence": best_result}
        if best_result == positive_conf:
            data["sentiment"] = Sentiment.POSITIVE
        elif best_result == neutral_conf:
            data["sentiment"] = Sentiment.NEUTRAL
        else:
            data["sentiment"] = Sentiment.NEGATIVE

        return data

    def _calculate_batch_confidence(self, count1, count2, count3 = 0) -> float:
        """
        Calculates confidence of sentiment using # of high confidence tweets
            for each sentiment.
        Calculates ratio of current sentiment versus other sentiments
        Then returns 1 - 1/(1+0.8*x), bounds between 0 and 1, if the ratio is 
        slightly higher then 0.5 the confidence will be 0.5
        """
        others = count2 + count3 + 0.0001
        x = count1/others
        return 1 - 1/(1+0.8*x)

    def find_adjective(sentiment: str) -> str:
        """Given a sentiment, returns a fitting adjective."""
        if sentiment == Sentiment.POSITIVE:
            random_positive_index = randrange(0, len(Sentiment.POSITIVE_WORDS))
            return Sentiment.POSITIVE_WORDS[random_positive_index]
        elif sentiment == Sentiment.NEUTRAL:
            random_neutral_index = randrange(0, len(Sentiment.NEUTRAL_WORDS))
            return Sentiment.POSITIVE_WORDS[random_neutral_index]
        elif sentiment == Sentiment.NEGATIVE:
            random_negative_index = randrange(0, len(Sentiment.NEGATIVE_WORDS))
            return Sentiment.POSITIVE_WORDS[random_negative_index]
    
        return "A non-real sentiment was passed to find_adjective()"

sentiment_classifier = SentimentClassifier()
