#!/usr/bin/python
import numpy as np
import os
#this function calculates the emission parameter
def cal_emission(count_pair,count_y):
    try:
        emission_para = (float(count_pair)/float(count_y))
    except:
        pass #return "divide by zero"
    return emission_para

#this function finds the tag and the times it appears and save it in a dictionary
def findTagDict(count_file):
    #dictTag = {}#dict()
    try:
        count_content = open(count_file)
    except:
        print "no such file"
    for count_line in count_content:
        count_list = count_line.strip().split(" ")
        if count_list[1] == "1-GRAM":
            if count_list[-1] not in dictTag:
                dictTag[count_list[-1]] = int(count_list[0])
            else:
                dictTag[count_list[-1]] += int(count_list[0])
    return dictTag

#this functin finds the word and the frequency of a word tagged aby a specific tag
def findWordDict(count_file):
    dictWord = {}#dict() or will pop dict() not callable error
    try:
        count_content = open(count_file)
    except:
        print "no such file"
    for count_line in count_content:
        count_list = count_line.strip().split(" ")
        word = count_list[-1]
        tag = count_list[2]
        number = count_list[0]
        if count_list[1] =="WORDTAG":
            #initialize
            if word not in dictWord:
                dictWord[word] = {}  
            #add element
            if tag not in dictWord[word]:
                dictWord[word][tag] = int(number)
            else:
                dictWord[word][tag] += int(number)
            
    return dictWord
           
#this function finds the maximum emission for the tage 
#and return a dictionary which values are lists
#and this dictionary stores the most possible word tag for each word
def maxEmisssion(dictWord,dictTag):
    dictMax = {}
    for word in dictWord:
        max_ratio = 0
        max_tag = ""
        for tag in dictWord[word]:
            dictWord[word][tag] = cal_emission(dictWord[word][tag],dictTag[tag])
            if dictWord[word][tag] >= max_ratio:
                max_ratio = dictWord[word][tag]
                max_tag = tag
                max_log =  np.log2(max_ratio)
            else:
                max_ratio = max_ratio
                max_tag = max_tag
                max_log =  np.log2(max_ratio)
        dictMax[word] = [max_tag,max_log]
    #print dictWord
    return dictMax


#this function makes prediction for the words in test data and save an output in txt
def prediction(test_input,output_file):
    try:
        test_data = open(test_input)
    except:
        print "no such file"
    try:
        output_data = open(output_file,'w')
    except:
        print "no such file"
    for test_line in test_data:
        if test_line == "\n":
            output = "\n"
        #print test_line.split(" ")
        elif test_line.strip() not in dictMax:
            original_word = test_line.strip()
            value = dictMax["_RARE_"][0]+" "+str(dictMax["_RARE_"][1])
            output = original_word + " "+ value +"\n"
        else:#lif test_line.strip() in dictMax:
            original_word = test_line.strip()
            value = dictMax[original_word][0]+" "+str(dictMax[original_word][1])
            output = original_word + " "+ value +"\n"
        output_data.write(output)
        #print output
if __name__=="__main__":
    #input and parameters
    #os.system("python2.7 count_freqs.py  ner_train_new.dat > ner_new.counts")
    count_file = "ner_rare.counts"
    #count_file = "ner_rare.counts"
    #count_file = "ner_multi.counts"
    test_input = "ner_dev.dat"
    #output = "4_2_multi.txt"
    #output = "4_2_rare.txt"
    output = "4_2.txt"
    dictTag = {}
    dictTag = findTagDict(count_file)
    dictWord = {}
    dictWord = findWordDict(count_file)
    dictMax = maxEmisssion(dictWord,dictTag)
    #print dictMax
    prediction(test_input,output)
    #print dictMax

