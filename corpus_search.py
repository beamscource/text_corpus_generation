# Author Eugen Klein, November 2020

import argparse
from tqdm import tqdm
import re
import os


def search(file_contents, **kwargs):

    input_column = kwargs['input_column']
    separator = kwargs['separator']

    if input_column:
        try:
            header = file_contents[0].strip().split(separator)
            column_indx = header.index(input_column)
        except:
            print('Specified column not found. Make sure the file has a header.')

    #expression = '[^a-zA-Z0-9 -\\.;<>/ =\'{}\\[\\]\\^\\?_\\\\|:\r\n~äöüß]{}'.format()
    #special_characters = re.compile('[^a-zA-Z0-9 -\\.;<>/ =\'{}\\[\\]\\^\\?_\\\\|:\r\n~äöüß]{4}')
    special_characters = re.compile('[^a-zA-Z0-9 \\-\'\\_\r\n~äöüÄÖÜß]{1,}')
    containing_words = re.compile('[a-zA-Z]*?[^a-zA-Z0-9 \\-\'\\_\r\n~äöüÄÖÜß]{1,}[a-zA-Z]*?')
    found_characters = []
    found_words = []

    for i, line in enumerate(tqdm(file_contents)):

        if input_column:
            try:
                line = line.split(separator)[column_indx]
            except:
                print('\nINFO: Broken line {} skipped.'.format(i+1))
                continue

        if re.search(special_characters, line):
            specials_in_line = re.findall(special_characters, line)
            for special in specials_in_line:
                if special not in found_characters:
                    found_characters.append(special + '\n')

            words_in_line = re.findall(special_characters, line)
            for word in words_in_line:
                if word not in found_words:
                    found_words.append(word + ' found in line ' + str(i+1) + '\n')

    return found_characters, found_words
    

def write_files(found_characters, found_words, source_location, special_file_name):
    
    # write updated file
    with open(os.path.join(source_location, special_file_name), 'w', \
        encoding='utf-8') as f:
        if found_characters:
            f.writelines('{}'.format(line) for line in found_characters)
        else:
            ('NOTHING FOUND\n\n')
        f.writelines('================= containing words ===================\n')
        if found_words:
            f.writelines('{}'.format(line) for line in found_words)
        else:
            f.writelines('NOTHING FOUND\n')

def main(args):
    
    source_location = args.file
    input_column = args.input_column
    separator = args.separator
    
    if os.path.isfile(source_location):
        
        with open(source_location, 'r', encoding='utf-8') as f:
            file_contents = f.readlines()

        source_location, file_name = os.path.split(source_location)
        found_characters, found_words = search(file_contents, input_column=input_column, \
            separator=separator)
        if input_column:
            special_file_name = file_name.split('.table')[0] + '.specials'
        else:
            special_file_name = file_name.split('.txt')[0] + '.specials'
        write_files(found_characters, found_words, source_location, special_file_name)

if __name__ == "__main__":

    ''' find special and broken characters in table and raw text files '''

    parser = argparse.ArgumentParser(description='Search table or raw text \
        files.')

    parser.add_argument('-f', '--file', required=True, \
        help="File to be searched.")
    parser.add_argument('-i', '--input_column', required=False, \
        help="Column to be searched.")
    parser.add_argument('-s', '--separator', default=':', \
        help="Separator to use for splitting columns. Default is set to colon.")

    args = parser.parse_args()

    main(args)