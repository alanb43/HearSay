import requests
import os
from typing import List, Tuple

class RelevancyAnalyzer:
    API_URL = 'https://api-inference.huggingface.co/models/sentence-transformers/msmarco-distilbert-base-tas-b'
    HEADERS = {'Authorization': f'Bearer {os.environ["HUGGINGFACE_API_KEY"]}'}

    def __init__(self):
        print('Initialized new RelevancyAnalyzer')

    def get_most_relevant_tweets(self, tweets: List[str], question: str, num_return_tweets: int) -> List[str]:
        data = self.__get_relevancy_scores(question, tweets)
        # Take only first num_return_tweets most relevant ones, and only include the tweet (not score)
        return_tweets = [x[1] for x in sorted(data, reverse=True)[:num_return_tweets]]
        return return_tweets

    def __get_relevancy_scores(self, question: str, answers: List[str]) -> List[Tuple[float, str]]:
        query_input = {
            'inputs': {
                'source_sentence': question,
                'sentences': answers
            }}
        data = self.__query_model(query_input)
        return [(data[x], answers[x]) for x in range(len(answers))]

    def __query_model(self, payload):
        response = requests.post(self.API_URL, headers=self.HEADERS, json=payload)
        return response.json()