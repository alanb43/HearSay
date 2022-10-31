from transformers import pipeline

class ResponseGenerator:
    """Generates Response using question and context given by tweets"""

    def __init__(self, model_name = "deepset/roberta-base-squad2"):
        self.nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

    def generate_response(self, qa_input):
        return self.nlp(qa_input)
