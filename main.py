from speech_manager import SpeechManager
from input_analyzer import InputAnalyzer
from tweet_snagger import TweetSnagger
from sentiment_classifier import SentimentClassifier, POSITIVE_SENTIMENT, NEGATIVE_SENTIMENT, NEUTRAL_SENTIMENT
from user_profile import UserProfile
from intents import Intents

import numpy as np
from random import randrange

speech_manager = SpeechManager()
input_analyzer = InputAnalyzer()
tweet_snagger = TweetSnagger()
sentiment_analyzer = SentimentClassifier()

def main():
    """Integrates systems to allow an end-to-end interaction."""
    user_profile = None
    while True:
        try:
            # Decide whether to take speech or text input
            talk_or_text = input('Would you like to SPEAK or TYPE a phrase (or QUIT)? (s/t/q): ')
            if talk_or_text == 'q':
                break
            elif talk_or_text == 's':
                utterance = speech_manager.speech_to_text()
            else:
                utterance = input('Input phrase: ')
            
            analysis = input_analyzer.analyze(utterance)
            # Get intents and entities
            primary_intent = analysis["primary_intent"]
            entities = analysis["entities"]
            # Determine entities/targets
            entity_words = [entity['word'] for entity in entities]
            
            # create new user profile
            if "profile" in primary_intent and user_profile is None:
                user_profile = create_profile()
            # intent is for user's favorite teams or players
            elif "favorite" in primary_intent and user_profile is not None:
                if "team" in primary_intent or "teams" in primary_intent:
                    team = user_profile.teams[randrange(0, len(user_profile.teams))]
                    tweets = tweet_snagger.snag_tweets([team], intent=Intents.TRADE, num_tweets=20)
                    
                elif "player" in primary_intent or "players" in primary_intent:
                    player = user_profile.players[randrange(0, len(user_profile.players))]
                    tweets = tweet_snagger.snag_tweets([player], intent="other", num_tweets=20)

                # add batch sentiment analysis
                
            # either a trade or injury check
            elif primary_intent != "other":
                tweets = tweet_snagger.snag_tweets(topics=entity_words, intent=primary_intent, num_tweets=1)
                # Speech/text output
                response = tweets[0]['content']
                print ('Response tweet:', response)
                # speech_manager.text_to_speech(response)
            # Deal with unknown intents TODO: Update this, I didn't update with the rest of the file
            else: 
                tweets = tweet_snagger.snag_tweets(entity_words, intent="other", num_tweets = 10)
                output = sentiment_analyzer.batch_analysis(tweets)
                sentiment, confidence = output["sentiment"], output["confidence"]
                if sentiment == POSITIVE_SENTIMENT:
                    print(entities[0]["word"] + " has a positive sentiment")
                elif sentiment == NEUTRAL_SENTIMENT:
                    print(entities[0]["word"] + " has a neutral sentiment")
                elif sentiment == NEGATIVE_SENTIMENT:
                    print(entities[0]["word"] + " has a negative sentiment")


        
        except Exception as e:
            print("Exception occurred:", e)


def create_profile() -> UserProfile:
    """Gathers and analyzes verbal input to make a user profile."""
    speech_manager.text_to_speech("What's your name?")
    name = speech_manager.speech_to_text()
    teams_q = f"Nice to meet you, {name}. Which teams do you support?"
    speech_manager.text_to_speech(teams_q)
    teams_input = speech_manager.speech_to_text()
    teams = [e['word'] for e in input_analyzer.extract_entities(teams_input)]
    players_q = f"Ah, a {teams[0]} fan I see. Have any favorite players?"
    speech_manager.text_to_speech(players_q)
    players_input = speech_manager.speech_to_text()
    players = [e['word'] for e in input_analyzer.extract_entities(players_input)]
    speech_manager.text_to_speech("Got it. I've set up your profile!")
    return UserProfile(name,teams,players)

if __name__ == "__main__":
    main()
