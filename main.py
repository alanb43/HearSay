from input_analyzer import InputAnalyzer
from tweet_snagger import TweetSnagger
from sentiment_classifier import SentimentClassifier
from flask import Flask, request, jsonify
from flask_cors import CORS
from response_generation import ResponseGenerator

import numpy as np
import json

app = Flask(__name__)
CORS(app)

input_analyzer = InputAnalyzer()
tweet_snagger = TweetSnagger()
sentiment_analyzer = SentimentClassifier()
response_generator = ResponseGenerator()

@app.route("/v1/text", methods=["POST"])
def main():
    """Integrates systems to allow an end-to-end interaction."""
    print(f"Received text request")
    try:
        utterance = request.get_json()["query"]
        
        print(f"Received utterance: {utterance}")
        analysis = input_analyzer.analyze(utterance)
        primary_intent, entities = analysis["primary_intent"], analysis["entities"]
        entity_words = [entity['word'] for entity in entities]
        tweets = tweet_snagger.snag_tweets(topics=entity_words, intent=primary_intent, num_tweets=50)
        # response = response_generator.generate_response(utterance, tweets)
        response = ""
        print(response)


    except Exception as e:
        print("Exception occurred:", e)
        return json.dumps({"response": "No one's talking about this, why don't you tweet it?"})

    print(json.dumps({"response": response}))
    return jsonify({"response": response})

if __name__ == "__main__":
    port = 5000
    print("Running server on port %d" % port)
    app.run(port=port, debug=True)
