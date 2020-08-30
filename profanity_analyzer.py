from rasa.nlu.components import Component 
from rasa.nlu import utils
from rasa.nlu.model import Metadata
import nltk
import os
from profanity_filter import ProfanityFilter

class ProfanityAnalyzer(Component):

    """A pre-trained sentiment component"""

    name = "profanity_analyzer"
    provides = ["entities"]
    requires = []
    defaults = {}
    language_list = ["en"]

    def __init__(self, component_config=None):
        super(ProfanityAnalyzer, self).__init__(component_config)

    def train(self, training_data, cfg, **kwargs):
        pass

    def convert_to_rasa(self, value, confidence): # value ve confidence "process" method'tan geliyor
        """Convert model output into the Rasa NLU compatible output format"""
        entity = {
            "value":value, # asagidaki process method'tran geliyor
            "confidence":confidence, # asagidan geliyor
            "entity": "profane_word", # entity ismini bu sekilde tanimliyoruz
            "extractor": "profanity_extractor"
        }

        return entity

    def process(self, message, **kwargs):
        # burada custom olarak ne yapmak istiyorsak tanimliyoruz
        pf = ProfanityFilter()
        text = message.text
        value = "na"
        confidence = 0
        #ornegin text = "This is shit."
        # Eger kelime kufurse confidence skor olarak 100 atiyoruz
        if pf.is_profane(text):
            tokens = text.split(" ")
            for token in tokens:
                if pf.is_profane(token):
                    value = token
                    confidence =100

        if value != 'na':
            entity = self.convert_to_rasa(value, confidence)
            message.set("entities", [entity], add_to_output=True)
        else:
            pass 

    #def persist(self, model_dir):
