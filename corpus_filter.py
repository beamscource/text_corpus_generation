# Author Eugen Klein, November 2020

import argparse
from tqdm import tqdm
import os


def filt(file_contents, **kwargs):

    ''' filter uterrances that are too long '''

    input_column = kwargs['input_column']
    separator = kwargs['separator']
    cut_off = kwargs['cut_off']

    if input_column:
        try:
            header = file_contents[0].strip().split(separator)
            column_indx = header.index(input_column)
        except:
            print('Specified column not found. Make sure the file has a header.')

        # skip header for table
        for i, line in enumerate(tqdm(file_contents[1:])):

            utterance = line.split(separator)[column_indx].split() 

            if len(utterance) > int(cut_off):
                    file_contents[i+1] = ''
    else:
        for i, line in enumerate(tqdm(file_contents)):

            utterance = line.split() 

            if len(utterance) > int(cut_off):
                    file_contents[i] = ''

    return file_contents

def write_file(updated_file_contents, source_location, updated_file_name):
    
    # write updated file
    with open(os.path.join(source_location, updated_file_name), 'w', \
        encoding='utf-8', newline="") as f:
        for line in updated_file_contents:
            if not line.isspace(): # skip blank lines here
                f.writelines("{}".format(line))
def main(args):
    
    source_location = args.file
    input_column = args.input_column
    cut_off = args.cut_off
    separator = args.separator
    file_suffix = args.file_suffix

    if os.path.isfile(source_location):
        
        with open(source_location, 'r', encoding='utf-8') as f:
            file_contents = f.readlines()

        source_location, file_name = os.path.split(source_location)
        updated_file_contents = filt(file_contents, input_column=input_column, \
            cut_off=cut_off, separator=separator)
        if input_column:
            updated_file_name = file_name.split('.table')[0] + file_suffix + '.table'
        else:
            updated_file_name = file_name.split('.txt')[0] + file_suffix + '.txt'
        write_file(updated_file_contents, source_location, updated_file_name)

if __name__ == "__main__":

    ''' filter utterances in table or raw text files '''

    parser = argparse.ArgumentParser(description='Filter table or raw text \
        files.')

    parser.add_argument('-f', '--file', required=True, \
        help="File to be filtered.")
    parser.add_argument('-i', '--input_column', required=False, \
        help="Column to be filtered.")
    parser.add_argument('-coff', '--cut_off', default=300, \
        help="Word limit for utterances to be filtered at.")
    parser.add_argument('-s', '--separator', default=':', \
        help="Separator to use for splitting columns. Default is set to colon.")
    parser.add_argument('-fs', '--file_suffix', default='_filt', \
        help="File suffix to save updated file.")

    args = parser.parse_args()

    main(args)