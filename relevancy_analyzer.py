import json
import requests
from config import HUGGING_FACE_API_KEY
from typing import List, Tuple

class RelevancyAnalyzer:
    api_url = "https://api-inference.huggingface.co/models/sentence-transformers/msmarco-distilbert-base-tas-b"
    headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}

    def __init__(self):
        print ("Initialized new RelevancyAnalyzer")

    def get_most_relevant_tweets(self, tweets: List[str], question: str, num_return_tweets: int) -> List[str]:
        data = self.__get_relevancy_scores(question, tweets)
        # Take only first num_return_tweets most relevant ones, and only include the tweet (not score)
        return_tweets = [x[1] for x in sorted(data, reverse=True)[:num_return_tweets]]
        return return_tweets

    def __get_relevancy_scores(self, question: str, answers: List[str]) -> List[Tuple[float, str]]:
        query_input = {
            "inputs": {
                "source_sentence": question,
                "sentences": answers
            }}
        data = self.__query_model(query_input)
        return [(data[x], answers[x]) for x in range(len(answers))]

    def __query_model(self, payload):
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.json()