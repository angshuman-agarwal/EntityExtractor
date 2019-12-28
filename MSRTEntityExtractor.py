import time
import json
import logging
import warnings
import os
import requests
from typing import Any, List, Optional, Text, Dict

from rasa.nlu.constants import MESSAGE_ENTITIES_ATTRIBUTE
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.extractors import EntityExtractor
from rasa.nlu.model import Metadata
from rasa.nlu.training_data import Message

import recognizers_suite as Recognizers
from recognizers_suite import Culture, ModelResult

import traceback

from rasa.nlu.components import Component
from rasa.nlu import utils
from rasa.nlu.model import Metadata
from rasa.nlu.extractors import EntityExtractor


logger = logging.getLogger(__name__)

class MSRTExtractor(Component):
    """
       Entity Extractor built using Microsoft's Recognizers Text Package.
    
       It provides robust recognition and resolution of entities like numbers,
       units, and date/time;
       
       for more info. check here:  https://github.com/microsoft/Recognizers-Text
    """

    def __init__(self, component_config=None):
        super(MSRTExtractor, self).__init__(component_config)

    def add_extractor_name(
            self, entities: List[Dict[Text, Any]]
        ) -> List[Dict[Text, Any]]:
        """
        Adds the Extractor name to the Message class during the prediction.
        """
        for entity in entities:
                entity["extractor"] = self.name
        return entities


    @staticmethod
    def convert_to_rasa(
        matches: List[Dict[Text, Any]]
        ) -> List[Dict[Text, Any]]:
        """
        Method to convert the extracted entities from Recognizer Text to Rasa Format.

        Once the recognizer model has parsed all the entities,
        then we can convert the extracted entities to rasa format.
        """
        extracted = []
        for match in matches:
            entity={}
            entity["start"]=  match["start"]      
            entity["end"]=  match["end"]
            entity["text"]=match["text"]
            entity["entity"]= match["type_name"]

            if "values" in match["resolution"]:
                
                
                if match["type_name"]=="datetimeV2.datetime":
                    entity["entity"]=match["resolution"]["values"][-1]["type"]
                    entity["value"]=match["resolution"]["values"][-1]["value"]

                elif match["type_name"]=="datetimeV2.date":
                    entity["entity"]=match["resolution"]["values"][-1]["type"]
                    entity["value"]=match["resolution"]["values"][-1]["value"]

                elif match["type_name"]=="datetimeV2.time":
                        entity["entity"]=match["resolution"]["values"][-1]["type"]
                        entity["value"]=match["resolution"]["values"][-1]["value"]  
                
                elif match["type_name"]=="datetimeV2.timerange" or match["type_name"]=="datetimeV2.datetimerange":
                    entity["entity"]=match["resolution"]["values"][-1]["type"]
                    entity["value"]={
                        "start_time":match["resolution"]["values"][-1]["start"],
                        "end_time":match["resolution"]["values"][-1]["end"]
                    }

                elif match["type_name"]=="datetimeV2.daterange":
                        entity["entity"]=match["resolution"]["values"][-1]["type"]
                        entity["value"]={}
                        if "start" in match["resolution"]["values"][-1]:
                            entity["value"].update({"start_date":match["resolution"]["values"][-1]["start"]})

                        if "end" in match["resolution"]["values"][-1]:
                             entity["value"].update({"end_date":match["resolution"]["values"][-1]["end"]})
                             
                        if "start" not in match["resolution"]["values"][-1] and "end" not in match["resolution"]["values"][-1]:
                            entity["value"]=match["resolution"]["values"][-1]
                    
                else:
                    entity["value"]=match["resolution"]["values"]
            else:
                entity["value"]=match["resolution"]["value"]

            extracted.append(entity)

        return extracted        

    @staticmethod
    def _parse_all_entities(user_input: str, 
        culture: str) -> List[Dict[Text, Any]]:
        """
        This is the main method that does the entity extraction work.

        For more details: https://github.com/Microsoft/Recognizers-Text/tree/master/Python#api-documentation
        """

        return [
            # Number recognizer - This function will find any number from the input
            # E.g "I have two apples" will return "2".
            Recognizers.recognize_number(user_input, culture),

            # Ordinal number recognizer - This function will find any ordinal number
            # E.g "eleventh" will return "11".
            Recognizers.recognize_ordinal(user_input, culture),

            # Percentage recognizer - This function will find any number presented as percentage
            # E.g "one hundred percents" will return "100%"
            Recognizers.recognize_percentage(user_input, culture),

            # Age recognizer - This function will find any age number presented
            # E.g "After ninety five years of age, perspectives change" will return
            # "95 Year"
            Recognizers.recognize_age(user_input, culture),

            # Currency recognizer - This function will find any currency presented
            # E.g "Interest expense in the 1988 third quarter was $ 75.3 million"
            # will return "75300000 Dollar"
            Recognizers.recognize_currency(user_input, culture),


            # Temperature recognizer - This function will find any temperature presented
            # E.g "Set the temperature to 30 degrees celsius" will return "30 C"
            Recognizers.recognize_temperature(user_input, culture),

            # DateTime recognizer - This function will find any Date even if its write in colloquial language -
            # E.g "I'll go back 8pm today" will return "2017-10-04 20:00:00"
            Recognizers.recognize_datetime(user_input, culture),

            # PhoneNumber recognizer will find any phone number presented
            # E.g "My phone number is ( 19 ) 38294427."
            Recognizers.recognize_phone_number(user_input, culture),

            # Email recognizer will find any phone number presented
            # E.g "Please write to me at Dave@abc.com for more information on task
            # #A1"
            Recognizers.recognize_email(user_input, culture),
        ]

    @staticmethod
    def _parse_entiities(self,text: Text,language: str) -> List[Dict[Text, Any]]:
            """pass the user input to the recognizer model to parse the entities.
            
            Required Parameter: 

            @user_input -> user entered text,
            
            @lanugage -> lanugage for prediction
            """

            try:
                results = self._parse_all_entities(text, language)
                # Flatten results
                results = [item for sublist in results for item in sublist]
                results=json.dumps( results, default=lambda o: o.__dict__, indent='\t', ensure_ascii=False)
                return self.convert_to_rasa(json.loads(results))
                
            except:
                logger.error(
                    "Failed to parse entities from recognizer model."
                    "Error: {}".format(traceback.format_exc())
                )
                return []

    def process(self, message, **kwargs):
        """Retrieve the text message, pass it to the text recognizer
            and append the extracted entities to the message class."""


        language = Culture.English
        extracted_entities = self._parse_entiities(self,message.text,language)
        extracted_entities = self.add_extractor_name(extracted_entities)

        message.set(
            MESSAGE_ENTITIES_ATTRIBUTE,
            message.get(MESSAGE_ENTITIES_ATTRIBUTE, []) + extracted_entities,
            add_to_output=True,
        )