"""
An extremely simple script to help with collection and labelling of sentiment 
training data. Simply adjust the parameters and run to quickly collect & label
data without having to do any of the writing yourself.

NOTE: please don't ever "commit" this file unless you've actually improved it
"""

from tweet_snagger import TweetSnagger
import json

#################################
TOPIC = "Mudryk"                # Change
INTENT = "trade"                # these
NUM_TWEETS = 10                 # things
#################################

FILENAME = "sentiment-analysis/dataset.json"
MODES = {
    "append": "a",
    "write": "w+",
    "read": "r"
}

ts = TweetSnagger()
tweets = ts.snag_tweets([TOPIC], intent=INTENT, num_tweets=NUM_TWEETS)

with open(FILENAME, mode=MODES["append"]) as fptr:
    for tweet in tweets:
        print(tweet["content"])
        label = input("label for this tweet: ")
        while 0 < int(label) > 2:
            label = input("try again, label for this tweet: ")
        
        obj = {
            "text": tweet["content"], 
            "labels": int(label)
        }

        fptr.write(json.dumps(obj) + '\n')
