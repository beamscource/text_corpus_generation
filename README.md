# text_corpus_generation
Helper scripts to generate and format text corpora for NLU training

For text generation, https://github.com/SimGus/Chatette is used

### create semsigs.sigs file in the following format
INTENT_1: entity_1 entity_2
INTENTS and "true" ENTITIES should be uppercase, synonyms should be lowercase
always include NO_INTENT with all ENTITIES

### generate chatette templates (intents.chatette + entities.dict) from semsigs file
compile_chatette_templates.py -s_s semsigs.sigs

### expand the chatette templates (intents.chatette + entities_dict.chatette)
- if no entities are provided in the .sigs file, no entities.dict is created
- you can use entities as synonym lists (for synonyms, spelling variants etc.)
- when defining a synonym entry in entities.dict, literal and canonical value have to be identical, e.g., phone=phone
- for true entities, literals have to map to canonical forms, e.g., phone=DEVICE, table=DEVICE

### generate output file as a markdown file
python -m chatette 'intents.chatette' -a rasamd

Furthermore, you'll find additional functions to clean text files.
