# EntityExtractor
Entity Extractor for Rasa using Microsoft [Recognizers Text](https://github.com/microsoft/Recognizers-Text/tree/master/Python) for extractig common entities like dates, time, currency, age, email id and others.

I have built the Entity Extactor as an alternative for [Duckling Entity Extractor](https://rasa.com/docs/rasa/nlu/components/#ducklinghttpextractor), since there some problems using Duckling as it requires one server running for entity extraction as well as it's not available directly on Windows system.


## How to setup?

*Note: Make sure you have already installed and setup the Rasa on your system*

- **Step 1** : Install the [Recognizer's suite](https://pypi.org/project/recognizers-text-suite/) with the following command: ```` pip install recognizers-text-suite ````

- **Step 2** : Copy the `MSRTEntityExtractor.py` file in your project directory:

    ![ScreenShot](https://github.com/JiteshGaikwad/EntityExtractor/blob/master/project_dir.png)

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

| Type             | Text                                      | Output                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|------------------|-------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Email Id**     | my email id is abcd@gmail.com             |  ````"entities": [         {             "start": 15,             "end": 28,             "text": "abcd@gmail.com",             "entity": "email",             "value": "abcd@gmail.com",             "extractor": "MSRTExtractor"         }     ] ````                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **DateTime**     | next Thursday at 8pm                      | ```` "entities": [         {             "start": 0,             "end": 3,             "text": "next",             "entity": "ordinal",             "value": "0",             "extractor": "MSRTExtractor"         },         {             "start": 0,             "end": 19,             "text": "next thursday at 8pm",             "entity": "datetime",             "value": "2020-01-02 20:00:00",             "extractor": "MSRTExtractor"         }     ] ````                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Date**         | 31st dec.                                 | ```` "entities" : [         {             "start" : 0 ,             "end" : 3 ,             "text" : "31st" ,             "entity" : "ordinal" ,             "value" : "31" ,             "extractor" : "MSRTExtractor"          },         {             "start" : 0 ,             "end" : 7 ,             "text" : "31st dec" ,             "entity" : "date" ,             "value" : "2019-12-31" ,             "extractor" : "MSRTExtractor"          }     ]    ````                                                                                                                                                                                                                                                                                                                                                                                                   |
| **Currency**     | Show me products below ₹5000              | ```` "entities" : [         {             "start" : 24 ,             "end" : 27 ,             "text" : "5000" ,             "entity" : "number" ,             "value" : "5000" ,             "extractor" : "MSRTExtractor"          },         {             "start" : 23 ,             "end" : 27 ,             "text" : "₹5000" ,             "entity" : "currency" ,             "value" : "5000" ,             "extractor" : "MSRTExtractor"          }     ],    ````                                                                                                                                                                                                                                                                                                                                                                                                  |
| **Phone Number** | my contact number is 1234567890           | ```` "entities" : [         {             "start" : 21 ,             "end" : 30 ,             "text" : "1234567890" ,             "entity" : "number" ,             "value" : "1234567890" ,             "extractor" : "MSRTExtractor"          },         {             "start" : 21 ,             "end" : 30 ,             "text" : "1234567890" ,             "entity" : "phonenumber" ,             "value" : "1234567890" ,             "extractor" : "MSRTExtractor"          }     ]    ````                                                                                                                                                                                                                                                                                                                                                                         |
| **Age**          | I am 23 years old                         | ```` "entities" : [         {             "start" : 5 ,             "end" : 6 ,             "text" : "23" ,             "entity" : "number" ,             "value" : "23" ,             "extractor" : "MSRTExtractor"          },         {             "start" : 5 ,             "end" : 16 ,             "text" : "23 years old" ,             "entity" : "age" ,             "value" : "23" ,             "extractor" : "MSRTExtractor"          },         {             "start" : 5 ,             "end" : 12 ,             "text" : "23 years" ,             "entity" : "datetimeV2.duration" ,             "value" : [                 {                     "timex" : "P23Y" ,                     "type" : "duration" ,                     "value" : "725328000"                  }             ],             "extractor" : "MSRTExtractor"          }     ]  ```` |
| **Number**       | I have two apples                         | ```` "entities" : [         {             "start" : 7 ,             "end" : 9 ,             "text" : "two" ,             "entity" : "number" ,             "value" : "2" ,             "extractor" : "MSRTExtractor"          }     ]  ````                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **Ordinal**      | 7th                                       | ````  "entities" : [         {             "start" : 0 ,             "end" : 2 ,             "text" : "7th" ,             "entity" : "ordinal" ,             "value" : "7" ,             "extractor" : "MSRTExtractor"          }     ]   ````                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **Percentage**   | one hundred percents                      | ````  "entities" : [         {             "start" : 0 ,             "end" : 10 ,             "text" : "one hundred" ,             "entity" : "number" ,             "value" : "100" ,             "extractor" : "MSRTExtractor"          },         {             "start" : 0 ,             "end" : 19 ,             "text" : "one hundred percents" ,             "entity" : "percentage" ,             "value" : "100%" ,             "extractor" : "MSRTExtractor"          }     ]    ````                                                                                                                                                                                                                                                                                                                                                                             |
| **Temperature**  | Set the temperature to 30 degrees celsius | ```` "entities" : [         {             "start" : 23 ,             "end" : 24 ,             "text" : "30" ,             "entity" : "number" ,             "value" : "30" ,             "extractor" : "MSRTExtractor"          },         {             "start" : 23 ,             "end" : 40 ,             "text" : "30 degrees celsius" ,             "entity" : "temperature" ,             "value" : "30" ,             "extractor" : "MSRTExtractor"          }     ]   ````                                                                                                                                                                                                                                                                                                                                                                                          |
| **Quarters**     | 1st Quarter of 2020                       | ```` "entities" : [         {             "start" : 15 ,             "end" : 18 ,             "text" : "2020" ,             "entity" : "number" ,             "value" : "2020" ,             "extractor" : "MSRTExtractor"          },         {             "start" : 0 ,             "end" : 2 ,             "text" : "1st" ,             "entity" : "ordinal" ,             "value" : "1" ,             "extractor" : "MSRTExtractor"          },         {             "start" : 0 ,             "end" : 18 ,             "text" : "1st quarter of 2020" ,             "entity" : "daterange" ,             "value" : {                 "start_date" : "2020-01-01" ,                 "end_date" : "2020-04-01"              },             "extractor" : "MSRTExtractor"          }     ]   ````                                                                       |

## Language Support


Currently I have added suppport for `English` language, if you want to add other language, just edit the [line](https://github.com/JiteshGaikwad/EntityExtractor/blob/b902bbc66a2510aa4ec9fce3eb80c8541fc8cd24/MSRTEntityExtractor.py#L194) here:

   ` language = Culture.English `
   
- **Chinese**: Culture.Chinese
- **Dutch**: Culture.Dutch
- **English**: Culture.English
- **French**: Culture.French
- **Italian**: Culture.Italian
- **Japanese:** Culture.Japanese
- **Korean**: Culture.Korean
- **Portuguese**: Culture.Portuguese
- **Spanish**: Culture.Spanish
- **Turkish**: Culture.Turkish
   
   For more info., check the [reference](https://github.com/microsoft/Recognizers-Text#supported-entities-across-cultures)


