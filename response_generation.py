from transformers import pipeline

class ResponseGenerator:
    """Generates Response using question and context given by tweets"""

    def __init__(self, model_name = "deepset/roberta-base-squad2"):
        self.nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

    def generate_response(self, qa_input):
        return self.nlp(qa_input)

    def __summarize_text(self, text_input: str) -> str:
        return 'Summarized Text'

    def __get_relevant_tweets(self, tweets_input: list[str]) -> list[str]:
        return ["Relevant Tweet"]

    def __get_question_answer(self, question: str, answer: str) -> str:
        return "Answer to Question"

    def __get_sentiment_analysis(self, tweets_input: list[str]) -> str:
        return "Sentiment"