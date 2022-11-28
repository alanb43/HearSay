from dataclasses import dataclass

@dataclass
class Sentiment:
    """
    Sentiment class here to simplify imports 
    (just import this class instead of a ton of constant variables.
    """
    # don't touch
    POSITIVE = "Positive"
    NEUTRAL = "Neutral"
    NEGATIVE = "Negative"
    # add if you feel necessary
    POSITIVE_WORDS = ["good", "pretty good", "solid", "great"]
    NEUTRAL_WORDS = ["alright", "okay", "decent", "kind of mid"]
    NEGATIVE_WORDS = ["poorly", "bad", "not good", "nothing right"]
