"""
To use, it's required that you:
1. Install git large-file-storage (https://git-lfs.github.com/)
2. Have pulled the model 'trained_model' down from remote using git lfs
"""

from transformers import pipeline

MODEL_DIR = 'entity_extraction/trained_model/'

class InputAnalyzer:
    """Extracts entities and intents from strings representing spoken utterances."""

    def __init__(self):
        self.pipeline = pipeline(
            task='ner',
            model=MODEL_DIR,
            tokenizer=MODEL_DIR,
            aggregation_strategy="simple"
        )
    
    def analyze(self, subject: str):
        """Analyzes input to determine/find intents and entities."""
        analysis = {
            "input": subject, # original, unmodified subject
            "intents": None, # maybe a pair of primary_intent, secondary_intent?
            "entities": None, # a dictionary of <entity, type> pairs
            "other": None # other information if we can extract it (adjectives, pronouns, etc)
        }
        
        analysis['entities'] = self._extract_entities(subject)
        # intents = self._extract_intents(subject)
        
        # process_entities(entities) #  get them in a suitable form for easy integration with
        # process_intents(intents)   #  twitter API / our system that handles twitter API?

        return analysis

    def _extract_entities(self, subject: str):
        """
        Finds entities within the subject string.
        Returns entities with prediction confidence % in a dictionary.
        Entity Types
            - PER: person
            - TEAM: team or organization
        """
        entity_dict = self.pipeline(subject)
        # maybe process the dict here to avoid passing along unneccessary info?
        return entity_dict
    
    def _extract_intents(self, subject: str):
        """
        Determine intent of subject string.
        Here for intent people to write, unless unnecessary
        """
