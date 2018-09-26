#! /usr/bin/python
import os
from tagger_utils.emission import Emission
from tagger_utils.transaction import Transactor
from tagger_utils.viterbi_model import Viterbi

if __name__ == "__main__":
    # Produces 5_2.txt, the tagged ner_dev.dat data in the same format as
    # 4_2.txt but tagged using the Viterbi tagger
    count_file_name = "ner_rare.counts"
    train_file_name = "ner_train_rare.dat"
    print "--Executing: python count_freqs.py {train} > {cnt}".format(train=train_file_name, cnt=count_file_name)
    os.system("python count_freqs.py {train} > {cnt}".format(train=train_file_name, cnt=count_file_name))
    transactor = Transactor(count_file_name)
    emission = Emission(count_file_name)
    print "--Input file: ner_dev.dat\n--Output file: 5_2.txt"
    print "--Doing"
    viterbi_obj = Viterbi("ner_dev.dat", file("5_2.txt", "w"), transactor, emission)
    viterbi_obj.run()
    print "--Done"
