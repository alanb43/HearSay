from transformers import pipeline
import requests
import os

# not paying for github LFS, but this fine-tuned model is local to
# repo owners' machines. for access to it, contact bera@umich.edu 
MODEL_DIR = 'entity_extraction/trained_model/'
# For those not using fine-tuned model, hugging-face api will be used
API_TOKEN = os.environ['HUGGINGFACE_API_KEY']
API_URL = 'https://api-inference.huggingface.co/models/Jean-Baptiste/camembert-ner'
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def query(utterance: str):
    """Finds entities in utterance using general camembert model via API."""
    payload = { "inputs": utterance }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

class EntityClassifier:
    """Performs NER classification using camembert."""
    def __init__(self):
        self.__ner = None
        self.fine_tuned = int(os.environ["FINE_TUNED"])
        if self.fine_tuned == 1:
            self.__ner = pipeline(
            task='ner',
            model=MODEL_DIR,
            tokenizer=MODEL_DIR,
            aggregation_strategy='simple'
        )
    
    def get_entities(self, subject: str) -> dict:
        """
        Finds entities within the subject string.
        Returns entities with prediction confidence % in a dictionary.
        Entity Types
            - PER: person
            - TEAM: team or organization
        """
        return self.__ner(subject) if self.fine_tuned == 1 else query(subject)
