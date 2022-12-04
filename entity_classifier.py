from utils import query, FINE_TUNED

# not paying for github LFS, but this fine-tuned model is local to
# repo owners' machines. for access to it, contact bera@umich.edu 
MODEL_DIR = 'entity_extraction/trained_model/'
# For those not using fine-tuned model, hugging-face api will be used
API_URL = 'https://api-inference.huggingface.co/models/Jean-Baptiste/camembert-ner'
if FINE_TUNED:
    from transformers import pipeline

class EntityClassifier:
    """Performs NER classification using camembert."""
    def __init__(self):
        self.__ner = None
        if FINE_TUNED == 1:
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
        print("getting entities")
        return self.__ner(subject) if FINE_TUNED == 1 else query(subject, API_URL)
