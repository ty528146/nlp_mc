#!/usr/bin/python
#this function calculate the emission parameter
import os
def cal_emission(file_content,x_word,y_tag):
    count_pair = 0
    #better initialize 
    count_pair = 0
    count_y = 0
    emission_para = 0
    #Looping over a file object
    for line in file_content:#type of line is str
        each_list =  line.strip().split(" ")#eachline is a list
        #print each_list
        if each_list[1] == "WORDTAG" and each_list[-1] == x_word and each_list[2] == y_tag:
            count_pair = each_list[0]
        if y_tag in each_list and each_list[1] == "WORDTAG":
            count_y += int(each_list[0])
    print count_y
    #print count_pair
    try:
        emission_para = float(count_pair)/float(count_y)
    except ZeroDivisionError as err:
        print err
    return emission_para

#this function replaces rare words in the original corpus file with _RARE_
#n is the number of counts beneath which a word in considered infrequent
def replace_rare(count_file,train_old,train_new,n):
    dict_all = dict()
    dict_rare = dict()
    try:
        file_content = open(count_file,"r") 
        #print file_content.readlines()
    except IOError:
        print "no such file exists"
        
    try:
        raw_data = open(train_old,"r") 
    except IOError:
        print "no such file exists"

    try:
        new_data = open(train_new,"w") 
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
            
    for raw_line in raw_data:
        raw_list = raw_line.strip().split(" ")
        if raw_list[0] in dict_rare:
         #   raw_line = raw_line.replace(raw_list[0],"_RARE_")#cannot directly write raw_line.replace(raw_list[0],"_RARE_")
        #new_data.write(raw_line)
            raw_list[0] = "_RARE_"
        new_data.write(" ".join(raw_list)+"\n")
        
if __name__=="__main__":
    #os.system("count_freqs.py  ner_train.dat > ner.counts")
    try:
        file_content = open("ner.counts","r") 
    except IOError:
        print "no such file exists"
    #test case
    y_tag = "I-ORG"
    x_word = "University"
    emission_para = cal_emission(file_content,x_word,y_tag)
    print emission_para
    #test case  
    train_old = "ner_train.dat"
    train_new = "ner_train_rare.dat"
    count_file = "ner.counts"
    replace_rare(count_file,train_old,train_new,5)