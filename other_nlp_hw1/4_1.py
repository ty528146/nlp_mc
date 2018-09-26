#! /usr/bin/python

from tagger_utils.freq_counter import FreqCount

if __name__ == '__main__':
    # Produces a new file: ner_train_rare.dat, the data file with _RARE_ words
    input_file_name = 'ner_train.dat'
    output_file_name = 'ner_train_rare.dat'
    input_file = file(input_file_name, "r")
    freq_count = FreqCount(input_file, file(output_file_name, "w"))
    freq_count.counter()
    freq_count.judger()
    print '--Input file: %s' % input_file_name
    freq_count.replacer(file(input_file_name, "r"))
    print '--Output File with _RARE_: %s' % output_file_name

