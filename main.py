from speech_manager import SpeechManager
from input_analyzer import InputAnalyzer
from tweet_snagger import TweetSnagger
from sentiment_classifier import SentimentClassifier
from openai_client import OpenAIClient
from intent import Intent

import os
import numpy as np

from dotenv import load_dotenv

load_dotenv()


def main():
    """Integrates systems to allow an end-to-end interaction."""
    speech_manager = SpeechManager()
    input_analyzer = InputAnalyzer()
    tweet_snagger = TweetSnagger()
    sentiment_analyzer = SentimentClassifier()
    openai_client = OpenAIClient(os.getenv('OPENAI_API_KEY'))
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
            intents = analysis["intents"]
            entities = analysis["entities"]

            # Determine primary intent
            max_score = np.argmax(np.array(intents["scores"]))
            if intents["scores"][max_score] > 0.3:
                primary_intent = intents["labels"][max_score]
            else:
                primary_intent = "other"

            # Determine entities/targets
            entity_words = [entity['word'] for entity in entities]

            # TODO: add all entities to topics and customize for intents
            if primary_intent != "other":
                tweets = tweet_snagger.snag_tweets(topics=entity_words, intent=primary_intent, num_tweets=10)
            else:
                tweets = tweet_snagger.snag_tweets(topics=entity_words, intent="other", num_tweets=10)

            # Find tweet that best matches our intent
            scored_tweets = [] # [("Hope Ronaldo recovers from his injury!", 0.953), ...]
            if primary_intent != 'other':
                for tweet in tweets:
                    analysis = input_analyzer.analyze(tweet['content'])
                    intents = analysis['intents']
                    idx = intents['labels'].index(primary_intent)
                    score = intents['scores'][idx]
                    scored_tweets.append((tweet['content'], score))
            scored_tweets.sort(key=lambda x: -x[1]) # sort high-to-low

            # Calculate a rumor rating
            rumor_score = None
            if primary_intent == Intent.INJURY:
                # Retrieve player name slot
                player_entities = [x for x in entities if x['entity_group'].lower() == 'per']
                if len(player_entities) == 0:
                    raise Exception('No player names found in query') # if we don't have a player, we need to query the user for it
                elif len(player_entities) == 2:
                    raise Exception('More than one player name in query') # if this happens, query user to specify who they're asking about
                player_name = player_entities[0]['word']

                # Compute rumor score
                rumor_score = 0
                for pair in scored_tweets:
                    text = pair[0]
                    intent_score = pair[1]
                    has_injury = openai_client.player_has_injury(player_name, text)
                    rumor_score += (1 if has_injury else 0) * intent_score # pretty basic weighting for now
                rumor_score /= len(scored_tweets)
            else:
                # add rumor scores for other intents
                pass

            if rumor_score != None:
                print("Rumor score: %.2f" % rumor_score)
                print("HearSay rates this rumor a %d out of 10." % int(rumor_score * 10 + 0.5))

            # Sentiment analysis
            output = np.zeros(3) # 0 - positive, 1 - neutral, 2 - negative
            for tweet in tweets:
                sentiment = sentiment_analyzer.analyze(tweet["content"])
                if sentiment[0]["label"] == "Neutral":
                    output[1] += 1
                elif sentiment[0]["label"] == "Positive":
                    output[0] += 1
                elif sentiment[0]["label"] == "Negative":
                    output[2] += 1
            idx = np.argmax(output)

            if idx == 0:
                print(entities[0]["word"] + " has a positive sentiment")
            elif idx == 1:
                print(entities[0]["word"] + " has a neutral sentiment")
            elif idx == 2:
                print(entities[0]["word"] + " has a negative sentiment")

            # Speech/text output
            response = scored_tweets[0][0]
            print ('Response tweet:', response)
            speech_manager.text_to_speech(response)
        
        except Exception as e:
            print("Exception occurred:", e)


if __name__ == "__main__":
    main()