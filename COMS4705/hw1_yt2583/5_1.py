#!/usr/bin/python
import numpy as np
def calcuLog(a,b):
    try:
        result = np.log(float(a)/float(b))
    except:
        print "divided by 0"
    return result

def createNgramDict(train_list):
    trainDict = {}
    train_key = ' '.join(train_list[2:])
    train_value = train_list[0]
    return train_key,train_value

#######cannot add trainDict1[train_key] = int(train_value) and return the whole dict because dict is stillbuiding 
####first buiding three dictionaries for 1 gram,bigram and trigram for faster speed ###################
def buildDictionary(input_file):
    try:
        train_data = open(input_file,'r')
    except IOException as err:
        print "no such file"
    trainDict1 = {}
    trainDict2 = {}
    trainDict3 = {}
    for train_sentence in train_data:
        train_list = train_sentence.strip().split(" ")
        if train_list[1] =="1-GRAM":
            train_key,train_value = createNgramDict(train_list)
            trainDict1[train_key] = int(train_value)
        elif train_list[1] == "2-GRAM":
            train_key,train_value = createNgramDict(train_list)
            trainDict2[train_key] = int(train_value)
        elif train_list[1] == "3-GRAM":
            train_key,train_value = createNgramDict(train_list)
            trainDict3[train_key] = int(train_value)
    return trainDict1,trainDict2,trainDict3
#####the q parameter is calculated by trigram divided by bigram########################################

def calQparameter(trigram_file,input_file,output_file):
    try:
        trigram_data = open(trigram_file,'r')
    except:
        print "no such file"
    try:
        output_data = open(output_file,'w')
    except:
        print "no such file!"
    trainDict1,trainDict2,trainDict3 = buildDictionary(input_file)
    for trigram_raw in trigram_data:
        trigram = trigram_raw.strip()
        bigram = ' '.join(trigram.split(" ")[0:2])
        if trigram_raw == "\n":
            output = "\n"
        else:
            try:
                count_tri = trainDict3[trigram]
            except KeyError:
                count_tri = 0
            try:
                count_bi = trainDict2[bigram]
            except KeyError:
                count_bi = 0
            if count_bi != 0:
                result = calcuLog(count_tri,count_bi)
            else:
                result = '+inf'
            output = trigram +" "+ str(count_tri)+" "+str(count_bi)
            output = trigram +" "+ str(result)+"\n"
        output_data.write(output)
        #print output
    '''print trainDict1    
    print "---------"
    print trainDict2
    print "---------"
    print trainDict3'''
    

if __name__ == "__main__":
    input_file = "ner_rare.counts"   
    trigram_file = "trigrams.txt"
    output_file = "5_1.txt"
    calQparameter(trigram_file,input_file,output_file)