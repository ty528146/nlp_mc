#! /usr/bin/python
from collections import defaultdict
from rare_split import RareSplit


class FreqCount(object):
    def __init__(self, input_file, output_file=None, RARE=False):
        # This class count the frequency of each word and filter out the _RARE_ words
        # If RARE set to True, FreqCount would use classes in rare_split to divide rare words into smaller classes
        self.input_file = input_file
        self.output_file = output_file
        self.RARE = RARE
        self.rare_set = set()
        self.dic = defaultdict(int)
        self.rare_split = RareSplit()

    def counter(self):
        l = self.input_file.readline()
        while l:
            line = l.strip()
            if line:  # Nonempty line
                fields = line.split(" ")
                word = " ".join(fields[:-1])
                self.dic[word] += 1
            l = self.input_file.readline()
        self.input_file.close()

    def judger(self, upper_bound=5):
        for k, v in self.dic.items():
            if v >= upper_bound:
                self.dic.pop(k)

    def replacer(self, original_file):
        if not self.output_file:
            import logging
            logging.info("--No output file!")
            return
        rare_file = self.output_file
        l = original_file.readline()
        while l:
            line = l.strip()
            if line:  # Nonempty line
                fields = line.split(" ")
                ne_tag = fields[-1]
                word = " ".join(fields[:-1])
                if word in self.dic:
                    if self.RARE:
                        rare_type = self.rare_split.get_type(word)
                    else:
                        rare_type = "_RARE_"
                    rare_file.write(rare_type + ' ' + ne_tag + '\n')
                else:
                    rare_file.write(l)
            else:  # Empty line
                rare_file.write(l)
            l = original_file.readline()
        original_file.close()
