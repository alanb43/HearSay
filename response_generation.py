from transformers import pipeline
from relevancy_analyzer import RelevancyAnalyzer
from typing import List

class ResponseGenerator:
    """Generates Response using question and context given by tweets"""

    def __init__(self, model_name = "deepset/roberta-base-squad2"):
        self.relevancy_analyzer = RelevancyAnalyzer()
        self.qa_model = pipeline('question-answering', model=model_name, tokenizer=model_name)

    def generate_response(self, question: str, tweets: List[str]) -> str:
        raw_tweets = [x['content'] for x in tweets]
        relevant_tweets = self.__get_relevant_tweets(question, raw_tweets)
        answer = self.__get_question_answer(question, '\n'.join(raw_tweets))
        response = f'''
        Here is a relevant tweet:\n{relevant_tweets[0]}
        Here is the answer to your question: {answer}
        '''
        return response

    def __summarize_text(self, text_input: str) -> str:
        return 'Summarized Text'

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