from input_analyzer import InputAnalyzer
from tweet_snagger import TweetSnagger
from sentiment_classifier import SentimentClassifier
from flask import Flask, request, jsonify
from flask_cors import CORS
from response_generation import ResponseGenerator
from profile_manager import ProfileManager
from data_classes.intents import Intents

application = Flask(__name__)
CORS(application)

input_analyzer = InputAnalyzer()
tweet_snagger = TweetSnagger()
sentiment_analyzer = SentimentClassifier()
response_generator = ResponseGenerator()
profile_manager = ProfileManager(input_analyzer, sentiment_analyzer, tweet_snagger, response_generator)
# First requestion breaks for some reason, so warming it up
# response_generator.generate_response("null", [{"content":"null"}])

def generate_response(utterance: str) -> str:
    """Integrates systems to allow an end-to-end interaction."""
    try:
        print(f"Received utterance: {utterance}")
        analysis = input_analyzer.analyze(utterance)
        primary_intent, entities = analysis["primary_intent"], analysis["entities"]
        print(primary_intent)        
        # if user is in process of creating a profile
        if profile_manager.create_profile_state.engaged:
            response = profile_manager.build_profile(utterance)
        # if user wants to create a profile
        elif primary_intent == Intents.PROFILE:
            if profile_manager.profile_exists():
                response = "You already set up a profile!"
            else:
                profile_manager.create_profile_state.engaged = True
                response = "What's your name?"
        # profiled user checking on their favorite teams or player
        elif "favorite" in utterance:
            if not profile_manager.profile_exists():
                response = "You haven't set up a profile!"
            elif primary_intent == Intents.FAV_TEAMS:
                response = profile_manager.get_info_about_favorites(True)
            else:
                response = profile_manager.get_info_about_favorites(False)
        # all other cases managed by response generator
        else:
            if len(entities) == 0:
                response = "I didn't capture that, would you mind trying again?"
                return response
            
            if "injured" in utterance:
                primary_intent = Intents.INJURY
            elif "trade" in utterance:
                primary_intent = Intents.TRADE

            entity_words = [entity['word'] for entity in entities]
            tweets = tweet_snagger.snag_tweets(topics=entity_words, intent=primary_intent, num_tweets=50)
            response = response_generator.generate_response(utterance, tweets)

    except Exception as e:
        print("Exception occurred:", e)
        response = "No one's talking about this, why don't you tweet it?"
        if profile_manager.create_profile_state.engaged:
            profile_manager.reset_profile()
            response = "I couldn't capture that. I've reset the profile."

    return response

@application.route("/v1/text", methods=["POST"])
def main():
    utterance = request.get_json()["query"]
    response = generate_response(utterance)
    res = jsonify({"response": response})
    print(res)
    return res

if __name__ == "__main__":
    application.run()
