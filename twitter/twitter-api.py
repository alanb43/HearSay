import snscrape.modules.twitter as twitter
import pandas as pd

author = "FabrizioRomano"
topic = "Sancho"
num_tweets = 100

query = f"""(from:{author}) {topic} -filter:replies -filter:retweets"""
tweets = []

for tweet in twitter.TwitterSearchScraper(query).get_items():
    if len(tweets) == num_tweets:
        break
    tweets.append([tweet.date, tweet.user.username, tweet.content])

df = pd.DataFrame(tweets, columns=['Date', 'Author', 'Tweet'])
print(df)
