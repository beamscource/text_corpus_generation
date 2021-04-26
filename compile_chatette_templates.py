# Author Eugen Klein, March 2021 

''' A script to compile templates for intents and entities files 
    required by Chatette to generate a synthetic text corpus.
    After template generation, use the intents and entities files
    to expand the carrier phrases. '''

import argparse
import os

def compile_templates(sem_sigs):

    carrier_phrases = []
    defined_entities_dict = []

    for sem_sig in sem_sigs:
        intent, entities = sem_sig.strip().split(':')
        defined_intent = '%[{}]\n'.format(intent.strip())
        if len(entities) > 0:
            defined_entities = ['    '] # indentation for defined intent block
            for entity in entities.split():
                defined_entity = '@[{}] '.format(entity.strip())
                defined_entities.append(defined_entity)
                # formatting of entity for entities dict
                defined_entity_for_dict = defined_entity + '\n    literal // canonical\n\n'
                defined_entities_dict.append(defined_entity_for_dict)
            # join all entity slots and add new lines
            defined_entities = ''.join(defined_entities).rstrip() + '\n\n'
        else:
            defined_entities = '   no entities\n\n'

        defined_phrase = defined_intent + defined_entities
        carrier_phrases.append(''.join(defined_phrase))

    return ''.join(carrier_phrases), ''.join(defined_entities_dict)

def write_intents_file(**kwargs):

    for key, value in kwargs.items():
        if key == 'carrier_phrases':
            carrier_phrases = kwargs[key]
        if key == 'file_path':
            file_path = kwargs[key]
        if key == 'write_entities':
            write_entities = kwargs[key]

    file_name = 'intents.chatette'
    with open(os.path.join(file_path, file_name), 'w', \
        encoding='utf-8') as f:
        for line in carrier_phrases:
            f.writelines("{}".format(line))
        # add reference to a file containing entity lists
        if write_entities:
            f.writelines("{}".format('|entities.dict'))

def write_entities_dict(entity_entries, file_path):

    file_name = 'entities.dict'
    with open(os.path.join(file_path, file_name), 'w', \
        encoding='utf-8') as f:
        for line in entity_entries:
            f.writelines("{}".format(line))

def main(args):

    ''' sem_sig_list is a file containing a list of semantic signatures
    (INTENTS: corresponding entities) which is used to compile initial
    carrier phrases file for Chatette. '''

    sem_sig_file = args.sem_sigs

    if os.path.isfile(sem_sig_file):
        
        with open(sem_sig_file, 'r', encoding='utf-8') as f:
            sem_sigs = f.readlines()

        file_path, sem_sig_file = os.path.split(sem_sig_file)
        carrier_phrases, entity_entries = compile_templates(sem_sigs)
        if len(entity_entries) == 0:
            write_intents_file(carrier_phrases=carrier_phrases, file_path=file_path, write_entities=0)
        else:
            write_intents_file(carrier_phrases=carrier_phrases, file_path=file_path, write_entities=1)
            write_entities_dict(entity_entries, file_path)
    else:
        print('INFO: No signature file found in the given directory.')

if __name__ == "__main__":

    ''' compile carrier phrases from a list of semantic signatures'''

    parser = argparse.ArgumentParser(description='Compile carrier phrases \
        for Chatette.')
    parser.add_argument('-s_s', '--sem_sigs', required=True, help="File \
        containing a list of semantic signatures.")

    args = parser.parse_args()

    main(args)