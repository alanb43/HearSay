from speech_manager import SpeechManager
from input_analyzer import InputAnalyzer
from tweet_snagger import TweetSnagger
from sentiment_classifier import SentimentClassifier, POSITIVE_SENTIMENT, NEGATIVE_SENTIMENT, NEUTRAL_SENTIMENT

import numpy as np

def main():
    """Integrates systems to allow an end-to-end interaction."""
    # speech_manager = SpeechManager()
    speech_manager = None
    input_analyzer = InputAnalyzer()
    tweet_snagger = TweetSnagger()
    sentiment_analyzer = SentimentClassifier()
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
            # Deal with known intents
            if primary_intent != "other":
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


if __name__ == "__main__":
    main()