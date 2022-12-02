"""
To use, it's required that you:
1. Install git large-file-storage (https://git-lfs.github.com/)
2. Have pulled the model 'trained_model' down from remote using git lfs
"""

from entity_classifier import EntityClassifier
from intent_classifier import IntentClassifier
from data_classes.intents import INTENTS

import os
import numpy as np

class InputAnalyzer:
    """Wrapper class for intent & entity extraction."""

    def __init__(self):
        self.__entity_classifier = EntityClassifier(os.environ["FINE_TUNED"])
        self.__intent_classifier = IntentClassifier(INTENTS)
        
    
    def analyze(self, subject: str):
        """
        Analyzes input to determine/find intents and entities.
        Returns dict of analysis in form:
        {
            "input": original subject input arg,
            "primary_intent": string of primary intent derived from classifier
            "entities": dict of entities derived from entity classifier
            "other": other information extracted (adjectives, pronouns, etc)
        }
        """
        analysis = {
            "input": subject, # original, unmodified subject
            "intents": None, # string
            "entities": None, # a dictionary of <entity, type> pairs
            "other": None # other info we may extract (adjectives,pronouns,etc)
        }
        
        analysis['entities'] = self.extract_entities(subject)
        analysis['primary_intent'] = self.extract_primary_intent(subject)

        return analysis

    def extract_entities(self, subject: str):
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
    
    def extract_primary_intent(self, subject: str):
        """
        Determine intent of subject string.
        Here for intent people to write, unless unnecessary
        """
        intent_dict = self.__intent_classifier.classify_intent(subject)
        primary_intent = "" # default
        max_score = np.argmax(np.array(intent_dict["scores"]))
        if intent_dict["scores"][max_score] > 0.6:
            primary_intent = intent_dict["labels"][max_score]
        return primary_intent
