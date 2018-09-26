#! /usr/bin/python
import math
from collections import defaultdict
from rare_split import RareSplit


class Emission(object):
    def __init__(self, input_file, RARE_TYPE=False):
        # This class would calculate the log prob from tag to word
        # If RARE_TYPE set to True, we would divide original _RARE_ type into more classes
        # ../6.py would set RARE_TYPE to True
        self.RARE_TYPE = RARE_TYPE
        if RARE_TYPE:
            self.rare_splitter = RareSplit()
        self.counter = defaultdict(dict)
        self.tag_map = defaultdict(int)
        self.input_file = input_file
        self.tagger = defaultdict(dict)
        self.collector()
        self.tagger_gen()

    def collector(self):
        with open(self.input_file, "r") as f:
            l = f.readline()
            while l:
                line = l.strip()
                if line:  # Nonempty line
                    fields = line.split(" ")
                    try:
                        if 'WORDTAG' in fields:
                            cnt, typ, tag, word = fields
                            self.counter[word].setdefault(tag, int(cnt))
                        elif '1-GRAM' in fields:
                            cnt, typ, tag = fields
                            self.tag_map[tag] = int(cnt)
                    except ValueError:
                        pass
                l = f.readline()

    def tagger_gen(self):
        for word, tags in self.counter.items():
            for tag, cnt in tags.items():
                self.tagger[word].setdefault(tag, math.log(float(cnt)/self.tag_map[tag]))

    def get_emission(self, word, tag):
        if not word in self.tagger:
            if self.RARE_TYPE:
                rare_word = self.rare_splitter.get_type(word)
                return self.tagger.get(rare_word).get(tag, float("-inf"))
            else:
                return self.tagger.get("_RARE_").get(tag, float("-inf"))
        return self.tagger.get(word).get(tag, float("-inf"))
