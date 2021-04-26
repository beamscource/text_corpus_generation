# Author Eugen Klein, November 2020

import argparse
from tqdm import tqdm
from collections import OrderedDict
from collections import Counter
import os


def count(file_contents, **kwargs):

    input_column = kwargs['input_column']
    separator = kwargs['separator']

    utts_uniq = OrderedDict()
    min_words = 1000
    max_words = 0
    total_words = 0
    below_five = 0
    below_fifteen = 0
    below_twentyfive = 0
    below_thirtyfive = 0
    below_max= 0

    if input_column:

        try:
            header = file_contents[0].strip().split(separator)
            column_indx = header.index(input_column)
        except:
            print('Specified column not found. Make sure the file has a header.')

    # skip header for now manually
    for line in tqdm(file_contents[1:]):

        # skip empty lines
        if line.isspace():
            continue

        if input_column:
            line = line.split(separator)[column_indx]

        line = line.strip()

        utts_uniq[line] = utts_uniq.get(line, 0) + 1

        num_words = len(line.split(' '))

        if num_words < 5:
            below_five += 1
        elif num_words > 4 and num_words < 15:
            below_fifteen += 1
        elif num_words > 14 and num_words < 25:
            below_twentyfive += 1
        elif num_words > 24 and num_words < 35:
            below_thirtyfive +=1
        else:
            below_max += 1 

        total_words += num_words

        if num_words < min_words:
            min_words = num_words

        if num_words > max_words:
            max_words = num_words

    # compute clusters
    # utterances = list(utts_uniq.items())
    # list_utterences = []
    # for utterance in utterances:
    #     list_utterences.append(utterance[0])

    # breakpoint()

    #Counter(words).most_common(10)


    num_utts = len(file_contents)-1
    num_utts_uniq = len(utts_uniq)
    mean_words_utt = round(total_words/num_utts, 2)
    min_words_utt = min_words
    max_words_utt = max_words

    below_five = round(below_five/num_utts*100, 2)
    below_fifteen = round(below_fifteen/num_utts*100, 2)
    below_twentyfive = round(below_twentyfive/num_utts*100, 2)
    below_thirtyfive = round(below_thirtyfive/num_utts*100, 2)
    below_max = round(below_max/num_utts*100, 2)

    stats = {'Number of utterances': num_utts, 'Number of unique utterances': num_utts_uniq, \
        'Average number of words per utterance': mean_words_utt, 'Number of min words per utterance': min_words_utt, \
        'Number of max words per utterance': max_words_utt, 'Percentage of utterances with less than five words': below_five, \
        'Percentage of utterances with number of words between five and fifteen': below_fifteen, \
        'Percentage of utterances with number of words between fifteen and twenty five': below_twentyfive, \
        'Percentage of utterances with number of words between twenty five and thirty five': below_twentyfive, \
        'Percentage of utterances with number of words above thirty five': below_max}

    return stats
    

def write_files(stats, source_location, stats_file_name):
    # write stats file

    with open(os.path.join(source_location, stats_file_name), 'w', \
        encoding='utf-8') as f:

        for key in stats:
            f.writelines("{}\n".format(key + ' ' + str(stats[key])))

def main(args):
    
    source_location = args.file
    input_column = args.input_column
    separator = args.separator

    if os.path.isfile(source_location):
        
        with open(source_location, 'r', encoding='utf-8') as f:
            file_contents = f.readlines()

        source_location, file_name = os.path.split(source_location)
        stats = count(file_contents, input_column=input_column, \
                separator=separator)
        stats_file_name = file_name.split('.table')[0] + '.stats'
        write_files(stats, source_location, stats_file_name)

if __name__ == "__main__":

    ''' compute word counts for utterances and utterance clusters'''

    parser = argparse.ArgumentParser(description='Compute stats for table columns \
        /raw text files.')

    parser.add_argument('-f', '--file', required=True,
        help="File to be analyzed.")
    parser.add_argument('-i', '--input_column', required=False, \
        help="Column to be cleaned. If not given, input file is processed as raw text.")
    parser.add_argument('-s', '--separator', default=':', \
        help="Separator to use for splitting columns. Default is set to colon.")

    args = parser.parse_args()

    main(args)