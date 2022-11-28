from input_analyzer import InputAnalyzer
from tweet_snagger import TweetSnagger
from tweet_searcher import TweetSearcher
from sentiment_classifier import SentimentClassifier, POSITIVE_SENTIMENT, NEGATIVE_SENTIMENT, NEUTRAL_SENTIMENT
from flask import Flask, request, jsonify
from flask_cors import CORS
from response_generation import ResponseGenerator

import numpy as np
import json

app = Flask(__name__)
CORS(app)

print("Initializing objects")

# input_analyzer = InputAnalyzer()
# tweet_snagger = TweetSnagger()
tweet_searcher = TweetSearcher()
# sentiment_analyzer = SentimentClassifier()
response_generator = ResponseGenerator()

print("Finished initializing objects")

def generate_response(utterance: str):
    try:
        tweets = tweet_searcher.get_tweets(utterance)
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
    app.run(port=port)
