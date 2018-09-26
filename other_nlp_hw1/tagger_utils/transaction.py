#! /usr/bin/python
import math
from collections import defaultdict


class Transactor(object):
    def __init__(self, input_file):
        # This class stands for calculating the q parameter, the prob form former tags to new tags
        self.input_file = input_file
        self.bigram_counter = defaultdict(dict)
        self.trigram_counter = defaultdict(dict)
        self.para_q = defaultdict(dict)  # q parameter in HMM model
        self.collector()
        self.para_gen()

    def collector(self):
        with open(self.input_file, "r") as f:
            l = f.readline()
            while l:
                line = l.strip()
                if line:  # Nonempty line
                    fields = line.split(" ")
                    if '2-GRAM' in fields:
                        cnt, typ, tag1, tag2 = fields
                        self.bigram_counter[tag1].setdefault(tag2, int(cnt))
                    elif '3-GRAM' in fields:
                        cnt, typ, tag1, tag2, tag3 = fields
                        self.trigram_counter[tag1].setdefault(tag2, dict())
                        self.trigram_counter[tag1][tag2].setdefault(tag3, int(cnt))
                l = f.readline()

    def para_gen(self):
        for tag1, vals1 in self.trigram_counter.items():
            for tag2, vals2 in vals1.items():
                for tag3, cnt in vals2.items():
                    cnt_denominator = self.bigram_counter[tag1][tag2]
                    self.para_q[tag1].setdefault(tag2, dict())
                    self.para_q[tag1][tag2].setdefault(tag3, math.log(float(cnt)/cnt_denominator))

    def get_transaction(self, tag_u, tag_v, tag_w):
        if tag_u not in self.para_q:
            return float("-inf")
        if tag_v not in self.para_q.get(tag_u):
            return float("-inf")
        if tag_w not in self.para_q.get(tag_u).get(tag_v):
            return float("-inf")
        return self.para_q.get(tag_u).get(tag_v).get(tag_w)

    def get_q(self):
        return self.para_q

    def printer(self, test_file, output_file):
        # print the log probs into output file
        l = test_file.readline()
        while l:
            line = l.strip()
            if line:  # Nonempty line
                tag1, tag2, tag3 = line.split(" ")
                cnt = self.trigram_counter[tag1][tag2][tag3]
                cnt_denominator = self.bigram_counter[tag1][tag2]
                prob = math.log(float(cnt) / cnt_denominator)
                output_file.write("{tag1} {tag2} {tag3} {prob}\n".format(
                    tag1=tag1, tag2=tag2, tag3=tag3, prob=prob))
            l = test_file.readline()
        test_file.close()
        output_file.close()

