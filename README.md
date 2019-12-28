# EntityExtractor
Entity Extractor for Rasa using Microsoft [Recognizers Text](https://github.com/microsoft/Recognizers-Text/tree/master/Python)

## How to setup?

*Note: Make sure you have already installed and setup the Rasa on your system*

- **Step 1** : Install the [Recognizer's suite](https://pypi.org/project/recognizers-text-suite/) with the following command: ```` pip install recognizers-text-suite ````
- **Step 2** : Copy the `MSRTEntityExtractor.py` file in your project directory:
- **Step 3** : Add the  reference of our Entity Extractor inside the Rasa NLU pipeline configuration file, as shown below:

````
# Configuration for Rasa NLU.
# https://rasa.com/docs/rasa/nlu/components/

language: "en"

pipeline:
- name: "WhitespaceTokenizer"
- name: "RegexFeaturizer"
- name: "CRFEntityExtractor"
- name: "EntitySynonymMapper"
- name: "CountVectorsFeaturizer"
- name: "EmbeddingIntentClassifier"
- name: "MSRTEntityExtractor.MSRTExtractor"

# Configuration for Rasa Core.
# https://rasa.com/docs/rasa/core/policies/
policies:
  - name: MemoizationPolicy
  - name: KerasPolicy
  - name: MappingPolicy

````
- **Step 4** : Now you can train your model & test for the Entity Extractor

## Samples

| Type             | Text                            | Output                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|------------------|---------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Email Id**     | my email id is abcd@gmail.com   |  ````"entities": [         {             "start": 15,             "end": 28,             "text": "abcd@gmail.com",             "entity": "email",             "value": "abcd@gmail.com",             "extractor": "MSRTExtractor"         }     ] ````                                                                                                                                                                                                                                              |
| **DateTime**     | next Thursday at 8pm            | ```` "entities": [         {             "start": 0,             "end": 3,             "text": "next",             "entity": "ordinal",             "value": "0",             "extractor": "MSRTExtractor"         },         {             "start": 0,             "end": 19,             "text": "next thursday at 8pm",             "entity": "datetime",             "value": "2020-01-02 20:00:00",             "extractor": "MSRTExtractor"         }     ] ````                              |
| **Date**         | 31st dec.                       | ```` "entities" : [         {             "start" : 0 ,             "end" : 3 ,             "text" : "31st" ,             "entity" : "ordinal" ,             "value" : "31" ,             "extractor" : "MSRTExtractor"          },         {             "start" : 0 ,             "end" : 7 ,             "text" : "31st dec" ,             "entity" : "date" ,             "value" : "2019-12-31" ,             "extractor" : "MSRTExtractor"          }     ]    ````                           |
| **Currency**     | Show me products below ₹5000    | ```` "entities" : [         {             "start" : 24 ,             "end" : 27 ,             "text" : "5000" ,             "entity" : "number" ,             "value" : "5000" ,             "extractor" : "MSRTExtractor"          },         {             "start" : 23 ,             "end" : 27 ,             "text" : "₹5000" ,             "entity" : "currency" ,             "value" : "5000" ,             "extractor" : "MSRTExtractor"          }     ],    ````                          |
| **Phone Number** | my contact number is 1234567890 | ```` "entities" : [         {             "start" : 21 ,             "end" : 30 ,             "text" : "1234567890" ,             "entity" : "number" ,             "value" : "1234567890" ,             "extractor" : "MSRTExtractor"          },         {             "start" : 21 ,             "end" : 30 ,             "text" : "1234567890" ,             "entity" : "phonenumber" ,             "value" : "1234567890" ,             "extractor" : "MSRTExtractor"          }     ]    ```` |                                                                                                                                                                                                                                                                                                                                    |
