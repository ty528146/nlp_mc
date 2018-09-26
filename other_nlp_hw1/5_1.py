#! /usr/bin/python
import os
from tagger_utils.transaction import Transactor


if __name__ == "__main__":
    #  produces 5_1.txt, the file containing trigrams and their respective parameters
    #  in the format wi_2, wi_1, w_i, logq(w_i | wi_2, wi_1)
    count_file_name = "ner_rare.counts"
    if not os.path.exists(count_file_name):
        os.system("python count_freqs.py {train} > {cnt}".format(train="ner_train_rare.dat", cnt=count_file_name))
    trainer = Transactor(count_file_name)
    trainer.collector()
    print "--Input file: trigrams.txt\n--Output file: 5_1.txt"
    print "--Doing"
    trainer.printer(file("trigrams.txt", "r"), file("5_1.txt", "w"))
    print "--Done"
