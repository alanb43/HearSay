from transformers import pipeline
from relevancy_analyzer import RelevancyAnalyzer
from summarizer import Summarizer
from typing import List
from openai_client import OpenAIClient
from config import OPENAI_API_KEY

openai_client = OpenAIClient(OPENAI_API_KEY)

NL = '\n'

class ResponseGenerator:
    """Generates Response using question and context given by tweets"""

    def __init__(self, model_name = "deepset/roberta-base-squad2"):
        self.relevancy_analyzer = RelevancyAnalyzer()
        self.qa_model = pipeline('question-answering', model=model_name, tokenizer=model_name)
        self.summarizer = Summarizer()

    def generate_response(self, question: str, tweets: List[str]) -> str:
        raw_tweets = [x['content'] for x in tweets]
        relevant_tweets = self.__get_relevant_tweets(question, raw_tweets)
        answer = self.__get_question_answer(question, '\n'.join(raw_tweets))
        summary = self.__summarize_text(relevant_tweets)[0]['summary_text']
        response = f"Here is a relevant tweet:{NL}{relevant_tweets[0]}{NL}Here is the answer to your question: {answer}{NL}Here is a summary: {summary}"
        return response

    def __summarize_text(self, text_input: List[str]) -> str:
        # return self.summarizer.summarize_tweets(text_input)
        return openai_client.query(f"Tweets:{NL}{NL.join(text_input)}{NL}Summary: ")

    def __get_relevant_tweets(self, question: str, tweets_input: List[str]) -> List[str]:
        return self.relevancy_analyzer.get_most_relevant_tweets(tweets_input, question, min(10, len(tweets_input)))

    def __get_question_answer(self, question: str, context: str) -> str:
        qa_input = {
            'question': question,
            'context': context
        }
        return self.qa_model(qa_input)['answer']

    def __get_sentiment_analysis(self, tweets_input: List[str]) -> str:
        return "Sentiment"