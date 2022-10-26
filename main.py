from speech_manager import SpeechManager
from input_analyzer import InputAnalyzer
from tweet_snagger import TweetSnagger


def main():
    """Integrates systems to allow an end-to-end interaction."""
    speech_manager = SpeechManager()
    input_analyzer = InputAnalyzer()
    tweet_snagger = TweetSnagger()

    try:
        utterance = speech_manager.speech_to_text()
        analysis = input_analyzer.analyze(utterance)
        
        intents = analysis["intents"]
        entities = analysis["entities"]
        # Determine primary intent
        primary_intent = "FIXME"
        # Determine best entities / targets?

        tweets = []
        if primary_intent == "injury":
            tweets = tweet_snagger.snag_tweets()
        elif primary_intent == "trade":
            tweets = tweet_snagger.snag_tweets()

        # Do something with the tweets, turn it into English that can be spoken
        response = ""
        # Speech output
        speech_manager.text_to_speech(response)

    except:
        print("Exception occurred")


if __name__ == "__main__":
    main()