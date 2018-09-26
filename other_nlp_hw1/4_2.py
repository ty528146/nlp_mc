#! /usr/bin/python

import os
from tagger_utils.emission import Emission


class Predictor(object):
    def __init__(self, tagger, input_file, output_file):
        self.tagger = tagger
        self.predict_file = input_file
        self.output_file = output_file

    def run(self):
        l = self.predict_file.readline()
        while l:
            line = l.strip()
            if line:  # Nonempty line
                fields = line.split(" ")
                word = fields[0]
                if word in self.tagger:
                    tags = self.tagger[word]
                else:
                    tags = self.tagger["_RARE_"]
                max_prob = -float("inf")
                for tag, prob in tags.items():
                    if prob > max_prob:
                        res = tag
                        max_prob = prob
                self.output_file.write("{word} {tag} {prob}\n".format(word=word, tag=res, prob=max_prob))
            else:
                self.output_file.write("\n")
            l = self.predict_file.readline()
        self.output_file.close()
        self.predict_file.close()


if __name__ == "__main__":
    # Produces 4_2.txt, the tagged ner_dev.dat data with the extra log likelihood
    # column
    train_file_name = 'ner_train_rare.dat'
    count_file_name = 'ner_rare.counts'
    print "--Input file with _RARE_ label: {inp}\n--Counts file: {outp}".format(
        inp=train_file_name, outp=count_file_name)
    print "--Executing: python count_freqs.py {inp} > {outp}".format(inp=train_file_name, outp=count_file_name)
    os.system("python count_freqs.py {inp} > {outp}".format(inp=train_file_name, outp=count_file_name))
    trainer = Emission(count_file_name)
    trainer.collector()
    trainer.tagger_gen()
    print "--Test file: ner_dev.dat"
    predictor = Predictor(trainer.tagger, file("ner_dev.dat", "r"), output_file=file("4_2.txt", "w"))
    print "--Output file: 4_2.txt"
    predictor.run()
    print "--Done"
