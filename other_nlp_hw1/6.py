#! /usr/bin/python
import os

from tagger_utils.emission import Emission
from tagger_utils.freq_counter import FreqCount
from tagger_utils.transaction import Transactor
from tagger_utils.viterbi_model import Viterbi


if __name__ == "__main__":
    # Produces 6.txt, the tagged ner_dev.dat data in the same format as 4_2.txt
    # and 5_2.txt but tagged using the improved Viterbi tagger by dividing _RARE_ class
    train_file_name = 'ner_train.dat'
    rare_splitted_file_name = 'ner_train_rare_splitted.dat'
    count_file = 'ner_splitted.counts'
    freq_counter = FreqCount(file(train_file_name, "r"), file(rare_splitted_file_name, "w"), RARE=True)
    freq_counter.counter()
    freq_counter.judger()
    freq_counter.replacer(file(train_file_name, "r"))
    print '--Generated file containing multiple class of rare words: %s' % rare_splitted_file_name
    print '--Executing: python count_freqs.py {rare_sp} > {cnt_file}'.format(
        rare_sp=rare_splitted_file_name, cnt_file=count_file)
    os.system("python count_freqs.py {rare_sp} > {cnt_file}".format(
        rare_sp=rare_splitted_file_name, cnt_file=count_file))

    transactor = Transactor(count_file)
    emission = Emission(count_file, RARE_TYPE=True)
    print "--Input: ner_dev.dat\n--Output: 6.txt\n--Doing"
    viterbi_obj = Viterbi("ner_dev.dat", file("6.txt", "w"), transactor, emission)
    viterbi_obj.run()
    print "--Done"
