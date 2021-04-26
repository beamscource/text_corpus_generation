# Author Eugen Klein, November 2020

import argparse
from tqdm import tqdm
import os


def filt(file_contents, i_column, separator):

    ''' extract a column '''

    try:
        header = file_contents[0].strip().split(separator)
        column_indx = header.index(i_column)
    except:
        print('Specified column not found. Make sure the file has a header.')

    # skip header for now manually
    for i, line in enumerate(tqdm(file_contents)):

        utterance = line.split(separator)[column_indx].split() 

        file_contents[i] = ' '.join(utterance).strip()

    #breakpoint()

    return file_contents

def write_file(updated_file_contents, source_location, updated_file_name):
    # write updated file

    with open(os.path.join(source_location, updated_file_name), 'w', \
        encoding='utf-8', newline="") as f:
        for line in updated_file_contents:
            if not line.isspace(): # skip blank lines here
                f.writelines("{}\n".format(line))
def main(args):
    
    source_location = args.file
    i_column = args.input_column
    separator = args.separator

    if os.path.isfile(source_location):
        
        with open(source_location, 'r', encoding='utf-8') as f:
            file_contents = f.readlines()

        source_location, file_name = os.path.split(source_location)
        updated_file_contents = filt(file_contents, i_column, separator)
        updated_file_name = file_name.split('.table')[0] + '_utts' + '.txt'
        write_file(updated_file_contents, source_location, updated_file_name)

if __name__ == "__main__":

    ''' extract a column and save as text file '''

    parser = argparse.ArgumentParser(description='Extract text column from table \
        files.')

    parser.add_argument('-f', '--file', required=True, help="File \
        to be extracted from.")
    parser.add_argument('-i', '--input_column', required=True, help="Column \
        to be etracted.")
    parser.add_argument('-s', '--separator', default=':', help="Separator \
        to use for splitting columns. Default is set to colon.")

    args = parser.parse_args()

    main(args)