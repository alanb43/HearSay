"""
To use, it's required that you:
1. Install git large-file-storage (https://git-lfs.github.com/)
2. Have pulled the model 'trained_model' down from remote using git lfs
"""

from entity_classifier import EntityClassifier
from intent_classifier import IntentClassifier
from transformers import pipeline

MODEL_DIR = 'entity_extraction/trained_model/'

class InputAnalyzer:
    """Wrapper class for intent & entity extraction."""

    def __init__(self):
        self.__entity_classifier = EntityClassifier()
        self.__intent_classifier = IntentClassifier(["trade", "injury"])
        
    
    def analyze(self, subject: str):
        """
        Analyzes input to determine/find intents and entities.
        Returns dict of analysis in form:
        {
            "input": original subject input arg,
            "intents": dict of intent(s) derived from intent classifier
            "entities": dict of entities derived from entity classifier
            "other": other information extracted (adjectives, pronouns, etc)
        }
        """
        analysis = {
            "input": subject, # original, unmodified subject
            "intents": None, # maybe a pair of primary_intent, secondary_intent?
            "entities": None, # a dictionary of <entity, type> pairs
            "other": None # other information if we can extract it (adjectives, pronouns, etc)
        }
        
        analysis['entities'] = self.__extract_entities(subject)
        analysis['intents'] = self.__extract_intents(subject)
        
        # process_entities(entities) #  get them in a suitable form for easy integration with
        # process_intents(intents)   #  twitter API / our system that handles twitter API?

        return analysis

    def __extract_entities(self, subject: str):
        """
        Finds entities within the subject string.
        Returns entities with prediction confidence % in a dictionary.
        Entity Types
            - PER: person
            - TEAM: team or organization
        """
        entity_dict = self.__entity_classifier.get_entities(subject)
        # maybe process the dict here to avoid passing along unneccessary info?
        return entity_dict
    
    def __extract_intents(self, subject: str):
        """
        Determine intent of subject string.
        Here for intent people to write, unless unnecessary
        """
        intent_dict = self.__intent_classifier.classify_intent(subject)
        # maybe process the dict here to avoid passing along unneccessary info?
        return intent_dict
