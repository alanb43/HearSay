from input_analyzer import InputAnalyzer
from tweet_snagger import TweetSnagger
from google_searcher import GoogleSearcher
from sentiment_classifier import SentimentClassifier, POSITIVE_SENTIMENT, NEGATIVE_SENTIMENT, NEUTRAL_SENTIMENT
from flask import Flask, request, jsonify
from flask_cors import CORS
from response_generation import ResponseGenerator

import numpy as np
import json

app = Flask(__name__)
CORS(app)

input_analyzer = InputAnalyzer()
tweet_snagger = TweetSnagger()
google_searcher = GoogleSearcher()
sentiment_analyzer = SentimentClassifier()
response_generator = ResponseGenerator()

def generate_response(utterance: str):
    try:
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

        for result in google_searcher.get_tweets(utterance):
            print(result)

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

        print(f"Retrieved tweets: {tweets}")

        # response = tweets[0]['content']
        response = response_generator.generate_response(utterance, tweets)

    except Exception as e:
        print("Exception occurred:", e)
        return "No one's talking about this, why don't you tweet it?"

    return response

@app.route("/v1/text", methods=["POST"])
def main():
    return jsonify({"response": generate_response(request.get_json()["query"])})

if __name__ == "__main__":
    port = 5000
    print("Running server on port %d" % port)
    app.run(port=port, debug=True)
