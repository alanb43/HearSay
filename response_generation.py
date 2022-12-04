from relevancy_analyzer import RelevancyAnalyzer
from summarizer import Summarizer
from sentiment_classifier import SentimentClassifier
from typing import List

import os
from utils import query

API_URL = 'https://api-inference.huggingface.co/models/deepset/roberta-base-squad2'
FINE_TUNED = int(os.environ["FINE_TUNED"])
if FINE_TUNED:
    from transformers import pipeline

class ResponseGenerator:
    """Generates Response using question and context given by tweets"""

    def __init__(self, model_name = "deepset/roberta-base-squad2"):
        self.relevancy_analyzer = RelevancyAnalyzer()
        if FINE_TUNED:
            self.qa_model = pipeline('question-answering', model=model_name, tokenizer=model_name)
    
        self.summarizer = Summarizer()
        self.sentiment_classifier = SentimentClassifier()

    def generate_response(self, question: str, tweets: List) -> str:
        print("generating response")
        raw_tweets = [x['content'] for x in tweets]
        relevant_tweets = self.__get_relevant_tweets(question, raw_tweets)
        answer = self.__get_question_answer(question, '\n'.join(relevant_tweets)).replace('\n', '')
        summary = self.summarize_text(relevant_tweets)[0]['summary_text'].replace('\n', '')
        sentiment = self.__get_sentiment_analysis(relevant_tweets)
        most_relevant_tweet = relevant_tweets[0].replace('\n', '')
        response = f'''
        {summary}
        The overall sentiment is {sentiment['sentiment']}.
        The short answer is "{answer}".
        The most relevant tweet is "{most_relevant_tweet}"
        '''
        return response

    def summarize_text(self, text_input: List[str]) -> str:
        return self.summarizer.summarize_tweets(text_input)

    def __get_relevant_tweets(self, question: str, tweets_input: List[str]) -> List[str]:
        return self.relevancy_analyzer.get_most_relevant_tweets(tweets_input, question, min(10, len(tweets_input)))

    def __get_question_answer(self, question: str, context: str) -> str:
        qa_input = {
            'question': question,
            'context': context
        }
        
        if FINE_TUNED:
            return self.qa_model(qa_input)['answer']
        
        return query(qa_input, API_URL)['answer']

    def __get_sentiment_analysis(self, tweets_input: List[str]):
        sentiment = self.sentiment_classifier.batch_analysis(tweets_input)
        if isinstance(sentiment, str):
            return {'sentiment': 'null', 'confidence': 'null'}
        return sentiment