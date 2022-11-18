import snscrape.modules.twitter as twitter
from intent_classifier import IntentClassifier
from intent import INTENTS

class TweetSnagger:
    """Snags sports tweets from Twitter."""

    def __init__(self):
        self.intent_classifier = IntentClassifier(INTENTS)

    def snag_tweets(self, topics, intent, authors = [], num_tweets = 5, replies = False, retweets = False, min_likes = 0):
        """
        Returns relevant tweets regarding input parameters. 
        Tweet format:
        {
            'url': str,
            'user': str,
            'content': str
        }
        """
        if intent == "other":
            query = self._make_query(topics, authors, replies, retweets)
        else:
            query = self._make_query(topics + [f'({intent})'], authors, replies, retweets)
        tweets = []
        print ("Making Twitter query:", query)
        for tweet in twitter.TwitterSearchScraper(query).get_items():
            if len(tweets) == num_tweets:
                break

            if self._verify_source(tweet.source) and self._verify_relevance(topics, tweet, intent) and tweet.likeCount >= min_likes:
                tweets.append({
                    'url': tweet.url,
                    'user': tweet.user.username, 
                    'content': tweet.content
                })
        
        return tweets
    
    def _verify_relevance(self, topics, tweet, intent):
        content = tweet.content
        if tweet.lang != 'en':
            print ("Bad tweet due to wrong language:", tweet.lang)
            return False
        # if (self.intent_classifier.classify_intent(content)['labels'][0] != intent or self.intent_classifier.classify_intent(content)['scores'][0] < 0.4) and intent != "other":
        #     print ("Bad tweet due to intent:", self.intent_classifier.classify_intent(content)['labels'][0], self.intent_classifier.classify_intent(content)['scores'][0])
        #     return False
        # for topic in topics:
        #     if topic.strip().lower() not in content.strip().lower():
        #         print ("Bad tweet due to missing topic:", topic)
        #         return False
        return True

    def _verify_source(self, source):
        """Returns whether source of tweet was human or not (99% confidence)."""
        return 'Web' in source or 'iPhone' in source or 'Android' in source

    def _make_query(self, topics, authors, replies = False, retweets = False):
        """Formats a query string given input."""
        author_q = ''
        # sep = 'AND' if everything else 'OR'
        if authors:
            for author in authors:
                author_q += f'from:{author} AND '

            author_q = '(' + author_q[:-5] + ') '

        topic_q = ''
        for topic in topics:
            topic_q += f'{topic} AND '
        
        topic_q = '(' + topic_q[:-5] + ') '

        query = author_q + topic_q
        
        query += '(lang:en) '
        if not replies:
            query += '-filter:replies '
        if not retweets:
            query += '-filter:retweets'
        
        return query
