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
- **Step 4**  Now you can train your model & test for the Entity Extractor

## Samples


