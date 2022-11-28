from input_analyzer import InputAnalyzer
from tweet_snagger import TweetSnagger
from sentiment_classifier import SentimentClassifier
from flask import Flask, request, jsonify
from flask_cors import CORS
from response_generation import ResponseGenerator
from profile_manager import ProfileManager

import numpy as np
import json

app = Flask(__name__)
CORS(app)

input_analyzer = InputAnalyzer()
tweet_snagger = TweetSnagger()
sentiment_analyzer = SentimentClassifier()
response_generator = ResponseGenerator()
#profile_manager = ProfileManager(input_analyzer, sentiment_analyzer, tweet_snagger)
# First requestion breaks for some reason, so warming it up
response_generator.generate_response("null", [{"content":"null"}])

@app.route("/v1/create", methods=["POST"])
def create_profile():
    data = request.get_json()
    name_, teams_, players_ = data["name"], data["teams"], data["players"]
    #profile_manager.create_profile(name_, teams_, players_)

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
        response = response_generator.generate_response(utterance, tweets)
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
