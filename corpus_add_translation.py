# Author Eugen Klein, November 2020

import argparse
from tqdm import tqdm
import re
import os


def augment(file_contents, i_column, o_column, separator, augmented_dict):

    ''' augment with english data '''

    try:
        header = file_contents[0].strip().split(separator)
        column_indx = header.index(i_column)
    except:
        print('Specified column not found. Make sure the file has a header.')


    for i, line in enumerate(tqdm(file_contents)):

        # write new header
        if i == 0:
            file_contents[i] = line.rstrip('\n') + separator + o_column + '\n'
            continue

        try:
            line = line.split(separator)[column_indx]
        except:
            print('\nINFO: Broken line {} skipped.'.format(i+1))
            continue

        try:
            file_contents[i] = file_contents[i].rstrip('\n') + separator + \
            augmented_dict[line] + '\n'
        except:
            file_contents[i] = file_contents[i].rstrip('\n') + separator + '\n'

    return file_contents

def create_dict(org_transcript, trans_transcript):

    org_transcript = tuple([utts.strip() for utts in org_transcript])
    trans_transcript = tuple([utts.strip() for utts in trans_transcript])
    keys = org_transcript
    values = trans_transcript
    augmented_dict = dict(zip(keys, values))

    return augmented_dict

def write_files(updated_file_contents, source_location, updated_file_name):
    # write updated file

    with open(os.path.join(source_location, updated_file_name), 'w', \
        encoding='utf-8') as f:
        f.writelines("{}".format(line) for line in updated_file_contents)

def main(args):
    
    source_location = args.file
    org_transcript = args.origin
    trans_transcript = args.translation
    i_column = args.input_column
    o_column = args.output_column
    separator = args.separator
    
    if os.path.isfile(source_location):
        
        with open(source_location, 'r', encoding='utf-8') as f:
            file_contents = f.readlines()

        with open(org_transcript, 'r', encoding='utf-8') as f:
            org_transcript_contents = f.readlines()

        with open(trans_transcript, 'r', encoding='utf-8') as f:
            trans_transcript_contents = f.readlines()

        source_location, file_name = os.path.split(source_location)
        augmented_dict = create_dict(org_transcript_contents, trans_transcript_contents)
        updated_file_contents = augment(file_contents, i_column, o_column, separator, augmented_dict)
        updated_file_name = file_name.split('.utd')[0] + '_trans_augmented.utd'
        write_files(updated_file_contents, source_location, updated_file_name)

if __name__ == "__main__":

    ''' Add a column with English translation to texts saved in a table. '''

    parser = argparse.ArgumentParser(description='Search text \
        files.')

    parser.add_argument('-f', '--file', required=True, help="File \
        to be cleaned.")
    parser.add_argument('-i', '--input_column', required=True, help="Column \
        to compare.")
    parser.add_argument('-o', '--output_column', default='en_translation', help="Column \
        translated data to be saved to.")
    parser.add_argument('-org', '--origin', required=True, help="File \
        containing original transcription.")
    parser.add_argument('-t', '--translation', required=True, help="File \
        containing the translated transcription.")
    parser.add_argument('-s', '--separator', default=':', help="Separator \
        to use for splitting columns. Default is set to colon.")

    args = parser.parse_args()

    main(args)