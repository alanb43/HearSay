from transformers import pipeline
from relevancy_analyzer import RelevancyAnalyzer
from typing import List

class ResponseGenerator:
    """Generates Response using question and context given by tweets"""

    def __init__(self, model_name = "deepset/roberta-base-squad2"):
        self.relevancy_analyzer = RelevancyAnalyzer()
        self.nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

    def generate_response(self, question: str, tweets: List[str]) -> str:
        raw_tweets = [x['content'] for x in tweets]
        relevant_tweets = self.__get_relevant_tweets(question, raw_tweets)
        return relevant_tweets[0]

    def __summarize_text(self, text_input: str) -> str:
        return 'Summarized Text'

    def __get_relevant_tweets(self, question: str, tweets_input: List[str]) -> List[str]:
        return self.relevancy_analyzer.get_most_relevant_tweets(tweets_input, question, 10)

    def __get_question_answer(self, question: str, answer: str) -> str:
        return "Answer to Question"

    def __get_sentiment_analysis(self, tweets_input: List[str]) -> str:
        return "Sentiment"