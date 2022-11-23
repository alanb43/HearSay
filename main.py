from speech_manager import SpeechManager
from input_analyzer import InputAnalyzer
from tweet_snagger import TweetSnagger
from sentiment_classifier import SentimentClassifier
from flask import Flask, request
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route("/v1/<method>", methods=["POST"])
def main(method):
    """Integrates systems to allow an end-to-end interaction."""
    print("Received request")
    speech_manager = SpeechManager()
    input_analyzer = InputAnalyzer()
    tweet_snagger = TweetSnagger()
    sentiment_analyzer = SentimentClassifier()
    # while True:
    try:
        # Decide whether to take speech or text input
        if method == "speech":
            utterance = speech_manager.speech_to_text()
        else:
            utterance = request.data["query"]
        
        print("Received utterance: {}" % utterance)

        analysis = input_analyzer.analyze(utterance)
        intents, entities = analysis["intents"], analysis["entities"]

        # Determine primary intent
        max_score = np.argmax(np.array(intents["scores"]))
        if intents["scores"][max_score] > 0.3:
            primary_intent = intents["labels"][max_score]
        else:
            primary_intent = "other"

        # Determine entities/targets
        entity_words = [entity['word'] for entity in entities]

        # TODO: add all entities to topics and customize for intents
        # Deal with known intents
        if primary_intent != "other":
            tweets = tweet_snagger.snag_tweets(topics=entity_words, intent=primary_intent, num_tweets=1)
        # Deal with unknown intents TODO: Update this, I didn't update with the rest of the file
        else: 
            tweets = tweet_snagger.snag_tweets(entity_words, intent="other", num_tweets = 100)
            output = np.zeros(3) # 0 - positive, 1 - neutral, 2 - negative
            for tweet in tweets:
                sentiment = sentiment_analyzer.analyze(tweet["content"])
                if sentiment[0]["label"] == "Neutral":
                    output[1] +=1
                elif sentiment[0]["label"] == "Positive":
                    output[0] +=1
                elif sentiment[0]["label"] == "Negative":
                    output[2] +=1

            idx = np.argmax(output)
            if idx == 0:
                print(entities[0]["word"] + " has a positive sentiment")
            elif idx == 1:
                print(entities[0]["word"] + " has a neutral sentiment")
            elif idx == 2:
                print(entities[0]["word"] + " has a negative sentiment")

        # Speech/text output
        response = tweets[0]['content']
        # print ('Response tweet:', response)
        speech_manager.text_to_speech(response)
    
    except Exception as e:
        print("Exception occurred:", e)


if __name__ == "__main__":
    port = 5000
    print("Running server on port %d" % port)
    app.run(port=port)
