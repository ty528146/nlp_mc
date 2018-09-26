#! /usr/bin/python
import re


class RareSplit(object):
    def __init__(self):
        # used for dividing rare words into subclasses
        pass

    def _is_numeric(self, word):
        pattern = re.compile(r'[^\d\.]+')
        result = re.search(pattern, word.replace("-", ""))
        if result:
            return False
        return True

    def _is_all_upper(self, word):
        if word.isupper():
            return True
        return False

    def _is_upper_on_first(self, word):
        if word and word[0].isupper():
            return True
        return False

    def _is_numeric_joint_by_dash(self, word):
        re_word = str(word)
        if self._is_numeric(re_word.replace("-", "")):
            return True
        return False

    def _is_upper_joint_by_dash(self, word):
        re_word = str(word)
        if self._is_all_upper(re_word.replace("-", "")):
            return True
        return False

    def _is_joint_by_dash_only(self, word):
        re_word = str(word)
        pattern = re.compile(r'[\W]+')
        result = re.search(pattern, re_word.replace("-", ""))
        if result:
            return False
        return True

    def get_type(self, word):
        if "_" in word:
            if self._is_numeric_joint_by_dash(word):
                return "_DASHED_NUM_"
            if self._is_upper_joint_by_dash(word):
                return "_DASHED_UPPER_"
            if self._is_joint_by_dash_only(word):
                return "_DASHED_"
        if len(word) == 1 and not word.isalpha():
            return "_CHAR_"
        word = word.replace(",", "").replace(".", "")
        if not word:
            return "_CHAR_"
        if word.isdigit():
            return "_DIGIT_"
        if word.isupper():
            return "_UPPER_"
        if word.islower():
            return "_LOWER_"
        if self._is_upper_on_first(word):
            return "_UPPER_FIRST_"
        if word.isalpha():
            return "_ALPHA_"
        return "_RARE_"
