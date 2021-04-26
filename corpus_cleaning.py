# Author Eugen Klein, November 2020

import argparse
from tqdm import tqdm
import re
import os

def clean(file_contents, **kwargs):

    input_column = kwargs['input_column']
    output_column = kwargs['output_column']
    separator = kwargs['separator']

    # broken letters/words

    umlaut_pattern = ['√é≈°', '√é¬°', '√ñ¬®', '√é√ω', '√§', '√é√ó', '√é¬ª', '√ç¬º', '√é¬º', '√é¬ú', '√º', '√ú', '√é¬∂', '√é¬ñ', '√∂']
    umlaut_replace = ['ä', 'ä', 'ä', 'ä', 'ä', 'ä', 'ü', 'ü', 'ü', 'ü', 'ü', 'ü', 'ö', 'ö', 'ö']

    sharp_pattern = ['√é¬∏', '√ü', '√é¬ü']
    sharp_replace = ['ß', 'ß', 'ß']

    vowels_pattern = ['√ñ¬∞']
    vowels_replace = ['i']

    currency_pattern = ['√¢¬¥¬¨']
    currency_replace = ['euro']

    diacritica_pattern = ['√¢¬†¬ô', '&#58;']
    diacritica_replace = ['\'', ':']

    other_pattern = ['√¢¬†¬ì']
    other_replace = ['-']

    # URLs (. and / have to be converted to _)
    url_pattern = re.compile('(https?://(?:www\\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\\.[^\\s]{2,}|www\\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\\.[^\\s]{2,}|https?://(?:www\\.|(?!www))[a-zA-Z0-9]+\\.[^\\s]{2,}|www\\.[a-zA-Z0-9]+\\.[^\\s]{2,})|https?://[a-zA-Z0-9\\./\\-?=&\\_]*|http?://[a-zA-Z0-9\\./\\-?=&\\_]*|http?:/[a-zA-Z0-9\\./\\-?=&\\_]*')
    mail_pattern = re.compile('[a-zA-Z0-9.!#$%&\'*+-/=?\\^_`{|}~-]+[ ]?@[ ]?[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*')

    # numbers
    cent_pattern = re.compile('[0-9]{1,2},[0-9]{1,2}')
    date_pattern = re.compile('[0-9]{1,2}\\.{1,2}[0-9]{1,2}\\.{0,2}[0-9]{0,4}')
    time_pattern = re.compile('[0-9]{1,2}:[0-9]{1,2}')
    
    # deletions
    invalid_pattern = re.compile('[^a-zA-Z0-9 \\-\'\\_:\r\n~äöüÄÖÜß]{1,}')

    # strip too many spaces and underscores
    space_pattern = re.compile(' +')
    underscore_pattern = re.compile('_+')
    underscore_trail_pattern = re.compile('_{1,}[ ]{1,}')

    multiple_hyphens = re.compile('-{2,}')

    if input_column:
        try:
            header = file_contents[0].strip().split(separator)
            num_col = len(header)
            column_indx = header.index(input_column)
        except:
            print('Specified column not found. Make sure the file has a header.')

    for i, line in enumerate(tqdm(file_contents)):

        # delete empty lines or single characters
        if line.isspace() or len(line) < 2:
            file_contents[i] = ''
            continue

        # assume table file
        if input_column:
            # write a new header
            if i == 0:
                file_contents[i] = line.rstrip('\n') + separator + output_column + '\n'
                continue

            columns = line.split(separator)
            
            # strip superfluous colons from input column
            # (cause bugs when working with resulting table)
            if len(columns) is not num_col:
                line_begin = line.split(':', column_indx)[0]
                line_finish = line.split(':', column_indx)[1]
                line_finish = line_finish.replace(':', '')
                line = line_begin + ':' + line_finish
                file_contents[i] = line.rstrip('\n')
                columns = line.split(separator)
                current_line = line = columns[column_indx]
                #current_line = line
            else:
                current_line = columns[column_indx]
                #current_line = line
        else:
            current_line = line

        # strip spaces and convert to lower case
        current_line = current_line.strip().lower()

        # broken letters/words
        for pattern, replace in zip(umlaut_pattern, umlaut_replace):
            if re.search(pattern, current_line):
                current_line = re.sub(pattern, replace, current_line)

        for pattern, replace in zip(sharp_pattern, sharp_replace):
            if re.search(pattern, current_line):
                current_line = re.sub(pattern, replace, current_line)

        for pattern, replace in zip(vowels_pattern, vowels_replace):
            if re.search(pattern, current_line):
                current_line = re.sub(pattern, replace, current_line)
        
        for pattern, replace in zip(currency_pattern, currency_replace):
            if re.search(pattern, current_line):
                current_line = re.sub(pattern, replace, current_line)

        for pattern, replace in zip(diacritica_pattern, diacritica_replace):
            if re.search(pattern, current_line):
                current_line = re.sub(pattern, replace, current_line)

        for pattern, replace in zip(other_pattern, other_replace):
            if re.search(pattern, current_line):
                current_line = re.sub(pattern, replace, current_line)

        # URLs, mails
        if re.search(url_pattern, current_line):
            urls = re.findall(url_pattern, current_line)
            for url in urls:
                replace = re.sub('[^a-zA-Z0-9 \\-]', '_', url)
                current_line = current_line.replace(url, replace)

        if re.search(mail_pattern, current_line):
            mails = re.findall(mail_pattern, current_line)
            for mail in mails:
                replace = re.sub('[^a-zA-Z0-9]', '_', mail)
                current_line = current_line.replace(mail, replace)

        # numbers
        if re.search(date_pattern, current_line):
            dates = re.findall(date_pattern, current_line)
            for date in dates:
                replace = re.sub('\\.', '_', date)
                current_line = current_line.replace(date, replace)

        if re.search(cent_pattern, current_line):
            amounts = re.findall(cent_pattern, current_line)
            for amount in amounts:
                replace = re.sub('\\.', '_', amount)
                replace = re.sub(',', '_', replace)
                current_line = current_line.replace(amount, replace)

        if re.search(time_pattern, current_line):
            times = re.findall(time_pattern, current_line)
            for time in times:
                replace = re.sub(':', '_', time)
                current_line = current_line.replace(time, replace)

        if re.search(invalid_pattern, current_line):
            current_line = re.sub(invalid_pattern, ' ', current_line)

        # delete groups of hyphens
        if re.search(multiple_hyphens, current_line):
            current_line = re.sub(multiple_hyphens, ' ', current_line)
        
        # trimming multiple spaces and underscores
        if re.search(underscore_pattern, current_line):
            current_line = re.sub(underscore_pattern, '_', current_line)

        if re.search(underscore_trail_pattern, current_line):
            current_line = re.sub(underscore_trail_pattern, ' ', current_line)

        if re.search(space_pattern, current_line):
            current_line = re.sub(space_pattern, ' ', current_line)

        # deal with trailing hyphens - 
        if re.search(' - ', current_line):
            current_line = re.sub(' - ', ' ', current_line)

        if re.search('- ', current_line) or re.search(' -', current_line):
            current_line = re.sub('- ', '-', current_line)
            current_line = re.sub(' -', '-', current_line)

        # delete ':' but not delimiter (fist occurence)
        if re.search(':', current_line):
            current_line = current_line.replace(':', '')

        if input_column:
            file_contents[i] = file_contents[i].rstrip('\n') + separator + \
                current_line.strip() + '\n'
        else:
            file_contents[i] = current_line + '\n'

    return file_contents

def write_file(updated_file_contents, source_location, updated_file_name):
    
    # write updated file
    with open(os.path.join(source_location, updated_file_name), 'w', \
        encoding='utf-8') as f:
        for line in updated_file_contents:
            f.writelines("{}".format(line))

def main(args):
    
    source_location = args.file
    input_column = args.input_column
    output_column = args.output_column
    separator = args.separator
    file_suffix = args.file_suffix

    if os.path.isfile(source_location):
        
        with open(source_location, 'r', encoding='utf-8') as f:
            file_contents = f.readlines()

        source_location, file_name = os.path.split(source_location)
        updated_file_contents = clean(file_contents, input_column=input_column, \
            output_column=output_column, separator=separator)
        if input_column:
            updated_file_name = file_name.split('.table')[0] + file_suffix + '.table'
        else:
            updated_file_name = file_name.split('.txt')[0] + file_suffix + '.txt'
        write_file(updated_file_contents, source_location, updated_file_name)

if __name__ == "__main__":

    ''' clean table and raw text files '''

    parser = argparse.ArgumentParser(description='Clean table columns/raw text \
        files.')

    parser.add_argument('-f', '--file', required=True, \
        help="File to be cleaned.")
    parser.add_argument('-i', '--input_column', required=False, \
        help="table column to be cleaned.")
    parser.add_argument('-o', '--output_column', default='transcription', \
        help="Column for cleaned data.")
    parser.add_argument('-s', '--separator', default=':', \
        help="Separator to use for splitting columns. Default is set to colon.")
    parser.add_argument('-fs', '--file_suffix', default='_clean', \
        help="File suffix to save updated file.")

    args = parser.parse_args()

    main(args)