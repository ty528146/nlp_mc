#! /usr/bin/python
from collections import defaultdict


class Viterbi(object):
    def __init__(self, input_file, output_file, transactor, emission):
        # This class implements the Viterbi algo
        self.input_file = input_file
        self.output_file = output_file
        self.transactor = transactor
        self.emission = emission

    def run(self):
        with open(self.input_file, "r") as f:
            l = f.readline()
            sentence = []
            while l:
                word = l.strip()
                if word:  # Nonempty line
                    sentence.append(word)
                    l = f.readline()
                    continue
                res = self.handler(sentence)
                for single_word, tag, prob in res:
                    self.output_file.write("{w} {t} {prob}\n".format(w=single_word, t=tag, prob=prob))
                self.output_file.write("\n")
                sentence = []
                l = f.readline()

    def handler(self, words_list):
        """
        Dynamic Programming
        :param words_list:
        :return: list[(word, tag, probability)]
        """
        n = len(words_list)
        S_1 = ["*"]
        S0 = list(S_1)
        S = ['I-LOC', 'B-ORG', 'I-PER', 'O', 'I-MISC', 'B-MISC', 'I-ORG', 'B-LOC']
        # special case when len(word_list) == 1
        if n == 1:
            word = words_list[0]
            prob = -1e10
            tag = ''
            for v in S:
                pi_w = 1
                q = self.transactor.get_transaction("*", "*", v)
                e = self.emission.get_emission(word, v)
                temp = pi_w + q + e
                if temp > prob:
                    prob, tag = temp, v
            return [(word, tag, prob)]
        dp_pi = [defaultdict(dict) for _ in range(n+1)]
        dp_pi[0]["*"]["*"] = 1
        dp_bp = [defaultdict(dict) for _ in range(n+1)]
        # w -> u -> v
        for k in range(1, n+1):
            if k == 1:
                u_set = S0
            else:
                u_set = S
            v_set = S
            for u in u_set:
                for v in v_set:
                    opt_val = float("-inf")
                    opt_w = ''
                    if k == 1:
                        w_set = S_1
                    elif k == 2:
                        w_set = S0
                    else:
                        w_set = S
                    for w in w_set:
                        pi_w = dp_pi[k-1][w][u]
                        q = self.transactor.get_transaction(w, u, v)
                        e = self.emission.get_emission(words_list[k-1], v)
                        temp_val = pi_w + q + e
                        if temp_val > opt_val:
                            opt_val = temp_val
                            opt_w = w
                    print opt_val
                    dp_pi[k][u].setdefault(v, opt_val)
                    dp_bp[k][u].setdefault(v, opt_w)
        if n == 1:
            set_n_1 = S0
            set_n = S
        else:
            set_n_1 = S
            set_n = S
        opt_u = ""
        opt_v = ""
        opt_val = float("-inf")
        for u in set_n_1:
            for v in set_n:
                q = self.transactor.get_transaction(u, v, "STOP")
                temp_val = q + dp_pi[n][u][v]
                if temp_val > opt_val:
                    opt_val = temp_val
                    opt_u = u
                    opt_v = v
        # back pointing
        tags = [opt_u, opt_v]
        probs = [-1e10] * n
        fst, sec = opt_u, opt_v
        for k in range(n-2, 0, -1):
            temp = dp_bp[k+2][fst][sec]
            tags.insert(0, temp)
            probs[k+1] = dp_pi[k+2][fst][sec]
            sec, fst = fst, temp
        probs[1] = dp_pi[2][tags[0]][tags[1]]
        probs[0] = dp_pi[1]["*"][tags[0]]
        return zip(words_list, tags, probs)


