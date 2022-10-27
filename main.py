from speech_manager import SpeechManager
from input_analyzer import InputAnalyzer
from tweet_snagger import TweetSnagger
from sentiment_classifier import SentimentClassifier

import numpy as np

def main():
    """Integrates systems to allow an end-to-end interaction."""
    #speech_manager = SpeechManager()
    input_analyzer = InputAnalyzer()
    tweet_snagger = TweetSnagger()
    sentiment_analyzer = SentimentClassifier()
    while True:
        try:
            #utterance = speech_manager.speech_to_text()
            utterance = input("Provide a sentence: ")
            if utterance=="q":
                break
            analysis = input_analyzer.analyze(utterance)
            
            intents = analysis["intents"]
            entities = analysis["entities"]
            # Determine primary intent
            max_score = np.argmax(np.array(intents["scores"]))
            if intents["scores"][max_score] > 0.5:
                primary_intent = intents["labels"][max_score]
            else:
                primary_intent = "other"
            # Determine best entities / targets?

            # TODO: add all entities to topics
            if primary_intent == "injury":
                tweets = tweet_snagger.snag_tweets([entities[0]["word"], "injury"])
            elif primary_intent == "trade":
                tweets = tweet_snagger.snag_tweets([entities[0]["word"], "trade"])
            elif primary_intent == "other":
                tweets = tweet_snagger.snag_tweets([entities[0]["word"]], num_tweets = 100)
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





            # print(tweets)
            
            # Do something with the tweets, turn it into English that can be spoken
            response = ""
            # Speech output
            #speech_manager.text_to_speech(response)

        except:
            print("Exception occurred")


if __name__ == "__main__":
    main()