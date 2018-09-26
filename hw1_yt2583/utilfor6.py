#!/usr/bin/python
import re
import os

#this function replaces rare words in the original corpus file with _RARE_
#n is the number of counts beneath which a word in considered infrequent
def genDict(count_file,n):
    dict_all = dict()
    dict_rare = dict()
    try:
        file_content = open(count_file,"r") 
        #print file_content.readlines()
    except IOError:
        print "no such file exists"
    for line in file_content:
        each_list = line.strip().split(" ")
        if each_list[1] == "WORDTAG":
            keys = each_list[-1]
            value = int(each_list[0])
            if keys in dict_all: #dict_all.keys():#this is very slow if use dict_all.keys()
                dict_all[keys] += value
            else:
                dict_all[keys] = value
    for i in dict_all:
        if dict_all[i] <n:
            dict_rare[i] = dict_all[i]
    return dict_rare        

def replace_rare(train_old,train_new):
    try:
        raw_data = open(train_old,"r") 
    except IOError:
        print "no such file exists"

    try:
        new_data = open(train_new,"w") 
    except IOError:
        print "no such file exists"
    pattern1 = r"\b[\d\.\-\"\'\,\?]*\b"
    for raw_line in raw_data:
        raw_list = raw_line.strip().split(" ")
        if raw_list[0] in dict_rare:
            if raw_list[0].isdigit():
                raw_list[0] = "_DIGIT_"
            elif raw_list[0].isupper():
                raw_list[0] = "_UPPER_"
            elif raw_list[0].islower():
                raw_list[0] = "_LOWER_"  
            elif raw_list[0] in re.findall(pattern1, raw_list[0]):
                raw_list[0] = "_NUMERALVALUE_" 
            else:
                raw_list[0] = "_RARE_"
            
            
        new_data.write(" ".join(raw_list)+"\n")
'''elif raw_list[0].replace(",","").replace("-","").isalpha():
                raw_list[0] = "_SPECIALSting_"   '''

try:
    file_content = open("ner.counts","r") 
except IOError:
    print "no such file exists"
train_old = "ner_train.dat"
train_new = "ner_train_multi.dat"
count_file = "ner.counts"
dict_rare = genDict(count_file,5)
replace_rare(train_old,train_new)
os.system("python2.7 count_freqs.py  ner_train_multi.dat > ner_multi.counts")