# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 13:03:52 2018

@author: umer
"""
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 11:37:57 2018

@author: umer
"""


import pandas as pd
import nltk
import numpy as np
import re, math
from collections import Counter
import timeit
from nltk.corpus import wordnet as wn
from langdetect import detect
from textblob import TextBlob
import operator

data=pd.read_csv('Book11.csv',converters={'QA': str,'ans':str},encoding = "ISO-8859-1")

stopwords = nltk.corpus.stopwords.words('english')


l1=len(data['ans'])

for x in range(0,l1):
    data['QA'][x]=data['QA'][x].lower()
   
tok11=[]
x=np.array(l1)

for y in range(0,l1):
    a = [word for word in nltk.word_tokenize(data['QA'][y]) if word not in stopwords]
    tok11.append(a)
    
for x in range(0,l1):
    for y in range(0,len(tok11[x])):  
        l2=len(tok11[x])
        for y1 in range(0,l2):
            for synset in wn.synsets(tok11[x][y1]):
                for lemma in synset.lemmas():
                    b=lemma.name()
                    tok11[x].append(b)
                    if(len(b)<12):    
                        tok11[x].append(b)

for z in range(0,l1):
   tok11[z]=list(set(tok11[z]))    
    
WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
    vec1 = Counter(WORD.findall(vec1))
    vec2 = Counter(WORD.findall(vec2))
    
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator
    
    

def DistJaccard(str1, str2):
    str1 = set(str1.split())
    str2 = set(str2.split())
    return float(len(str1 & str2)) / len(str1 | str2)

def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)

text1 = 'I like cat'
text2 = 'I like dog'



# Function to get the correct spelling
def remove_spell_errors(text):
    b = TextBlob(text)
    return b.correct()
#s

#a=2
#if(a):
    
print("type quit to stop")    
def mine():        
    text3 = input('Ask question\n')
    start = timeit.default_timer()
    text5 =remove_spell_errors(text3)
    text4= [word for word in nltk.word_tokenize(text3) if word not in stopwords]

    dis=np.array

    diss=[]
    for i in range(0,l1):
        dis1=float(get_cosine(str(tok11[i]),str(text4)))
        #dis2=float(DistJaccard(str(tok11[i]),str(text4)))
    #dis3=((dis1+dis2)/2)
        diss.append(dis1)

    index, value = max(enumerate(diss), key=operator.itemgetter(1))
    stop = timeit.default_timer()
    
    #print(value)
    if(value>0.0001):
        print(data['ans'][index])
        print(stop-start)
    
    else:
        print('ask another')    
    
    if text3!='quit':
        mine()
    
    
    
    return None

mine()
    
#print(stop-start)
#print(tok11)    