#!/usr/bin/python
import numpy as np
import time
import re
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

def calQparameter(trigram_each):
    trigram = trigram_each.strip()
    bigram = ' '.join(trigram.split(" ")[0:2])
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
        result = float('-inf')
    return result
    #print output
    
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
    #print dictTag
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
    for word in dictWord:
        max_ratio = 0
        max_tag = ""
        for tag in dictWord[word]:
            dictWord[word][tag] = np.log(cal_emission(dictWord[word][tag],dictTag[tag]))
    #print dictWord        
    return dictWord

def findEmission(word_input,tag_input):
    pattern1 = r"\b[\d\.\-\"\'\,\?]*\b"
    if word_input.strip() not in dictWord:
        original_word = word_input.strip()
        if original_word.isdigit():
            try:
                value = dictWord["_DIGIT_"][tag_input]
            except:
                value = float("-inf")
        elif original_word.isupper():
            try:
                value = dictWord["_UPPER_"][tag_input]
            except:
                value = float("-inf")
        elif original_word.islower():
            try:
                value = dictWord["_LOWER_"][tag_input]
            except:
                value = float("-inf")
        elif original_word in re.findall(pattern1, original_word):
            try:
                value = dictWord["_NUMERALVALUE_"][tag_input]
            except:
                value = float("-inf")
        else:
            try:
                value = dictWord["_RARE_"][tag_input]
            except:
                value = float("-inf")

    else:#lif test_line.strip() in dictMax://cannot use word and tag because they are the lastelement itmes keys and values
        original_word = word_input.strip()
        try:
            value = dictWord[original_word][tag_input]
        except:
            value = float("-inf")
    return value


           

def Viterbi(sentence):
    #initialization
    n = len(sentence)
    tag_sequence = []
    tag_value = []
    pI = {}
    K_n1 = ['*']
    K_0 = ['*']
    K = ['I-LOC', 'B-ORG', 'I-PER', 'O', 'I-MISC', 'B-MISC', 'I-ORG', 'B-LOC']
    #keys = str(position)","+u+","+v
    pI['0,*,*'] = 0# only store the maximum value corresponding to each position given u and v
    bp = {}
    ###corner case must be taken into consideration or the "0,," in the step 2 and 3 will be generated
    #must consider n==1
    if n == 1:
        optimal_val0 = float("-inf")
        optimal_tag = ''
        for v in K:
            trigram_0 = "*"+" "+"*"+" "+str(v)
            q = calQparameter(trigram_0)
            word_input = sentence[0]
            tag_input = str(v)
            e = findEmission(word_input,tag_input) 
            TEMP = pI['0,*,*']+q+e
            if TEMP > optimal_val0:
                optimal_val0 = TEMP
                optimal_tag = v
        return [optimal_tag],[str(optimal_val0)]
    #########################the first step of Viterbi##################
    for k in range(1,n+1):
        Vk = K
        if k == 1:
            Uk = K_0
            Wk = K_n1    
        elif k == 2:
            Uk = K
            Wk = K_0
        else:
            Uk = K
            Wk = K
        for u in Uk:
            for v in Vk:
                optimal_val = float("-inf")
                optimal_w = ''
                #make u v as given condition,change the value of Wk
                for w in Wk:
                    trigram_each = str(w)+" "+str(u)+" "+str(v)
                    q = calQparameter(trigram_each)
                    word_input = sentence[k-1]
                    tag_input = str(v)
                    e = findEmission(word_input,tag_input) 
                    key_last = str(k-1)+","+str(w)+","+str(u)
                    tmp = float(pI[key_last]) + q + e
                    #print tmp
                    if tmp > optimal_val:
                        optimal_val = tmp
                        optimal_w = w
                    else:
                        optimal_val = optimal_val
                        optimal_w = optimal_w
                key = str(k)+","+str(u)+","+str(v)
                pI[key] = optimal_val
                bp[key] = optimal_w
    
    ##########################step 2 of Viterbi Algorithm######################
    max_u = ""
    max_v = ""
    max_value = float("-inf")
    for u in K:
        for v in K:
            trigram_each = str(u)+" "+str(v)+" "+"STOP"
            q = calQparameter(trigram_each)
            key_fin = str(n)+","+str(u)+","+str(v)
            temp = pI[key_fin] + q
            if temp > max_value:
                max_value = temp
                max_u = u
                max_v = v
    #print pI
    #print bp
    tag_sequence.insert(0,max_v)
    tag_sequence.insert(0,max_u)
    ######################step 3 of Viterbi Algorithm#########################
    #insert all y sequence backwards
    #insert n~2 sequence of pi values backwards
    for k in range(n-2,0,-1):
        key_bp = str(k+2)+","+str(tag_sequence[0])+","+str(tag_sequence[1])
        #print key_bp
        tag_value.insert(0,str(pI[key_bp]))
        y_k = bp[key_bp]
        #print y_k
        tag_sequence.insert(0,y_k)
        #print len(tag_sequence)
    #insert the second value of pi
    key1 = str(2)+","+str(tag_sequence[0])+","+str(tag_sequence[1])
    tag_value.insert(0,str(pI[key1]))
    #insert the first value of pi
    key0 = str(1)+","+"*"+","+str(tag_sequence[0])
    tag_value.insert(0,str(pI[key0]))
    return tag_sequence,tag_value
                

def testFile(test_file):
    word_list = []
    sentence_list = []
    try:
        testdata = open(test_file,'r')
    except:
        print "no such file"
    for each_word_raw in testdata:
        if each_word_raw != "\n":
            each_word = each_word_raw.strip()
            word_list.append(each_word)
        else:
            sentence_list.append(word_list)
            word_list = []
    return sentence_list
        

if __name__ == "__main__":
    input_file = "ner_rare_multi.counts"  
    test_file = "ner_dev.dat"
    t_start = time.time()
    trainDict1,trainDict2,trainDict3 = buildDictionary(input_file)
    dictTag = {}
    dictTag = findTagDict(input_file)
    dictWord = {}
    dictWord = findWordDict(input_file)
    sentence_list = testFile(test_file)
    outputfile = open("6.txt","w")
    for word_list in sentence_list:
        tag_sequence,tag_value = Viterbi(word_list)
        tuple_sentence = zip(word_list,tag_sequence,tag_value)
        for tuple_word in tuple_sentence:
            output = " ".join(tuple_word)+"\n"
            outputfile.write(output)
            print output
        outputfile.write("\n")
        print "\n"