from transformers import pipeline

MODEL_DIR = 'entity_extraction/trained_model/'

class EntityClassifier:
    """Performs NER classification using camembert."""
    def __init__(self):
        self.__ner_pipeline = pipeline(
            task='ner',
            model=MODEL_DIR,
            tokenizer=MODEL_DIR,
            aggregation_strategy="simple"
        )
    
    def get_entities(self, subject: str) -> dict:
        """
        Finds entities within the subject string.
        Returns entities with prediction confidence % in a dictionary.
        Entity Types
            - PER: person
            - TEAM: team or organization
        """
        return self.__ner_pipeline(subject)
