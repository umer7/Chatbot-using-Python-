# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 17:38:35 2018

@author: umer
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 16:33:08 2018

@author: umer
"""
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import pandas as pd
import nltk
import numpy as np
import re, math
from collections import Counter
import timeit
from nltk.corpus import wordnet as wn



data=pd.read_csv('Book11.csv',converters={'QA': str,'ans':str})

l1=len(data['ans'])

for x in range(0,5):
    data['QA'][x]=data['QA'][x].lower()
   # print(data['QA'][x])
    
stopwords = nltk.corpus.stopwords.words('english')
    
tok11=[]
x=np.array(l1)

for y in range(0,l1):
    a = [word for word in nltk.word_tokenize(data['QA'][y]) if word not in stopwords]
    tok11.append(a)


for x in range(0,l1):
    for y in range(0,len(tok11[x])):  
        for synset in wn.synsets(tok11[x][1]):
            for lemma in synset.lemmas():
                b=lemma.name()
                #print (b)
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
#text3='What is the Eligibility criteria'

text3 = input('What is you question\n')
#print(text5)

text4= [word for word in nltk.word_tokenize(text3) if word not in stopwords]

start = timeit.default_timer()
cosine = get_cosine(text1, text2)
stop = timeit.default_timer()

start2 = timeit.default_timer()
dist = DistJaccard(text1,text2)
stop2 = timeit.default_timer()

dis=np.array


diss=[]
for i in range(0,5):
    dis1=float(get_cosine(str(tok11[i]),str(text4)))
    dis2=float(DistJaccard(str(tok11[i]),str(text4)))
    dis3=((dis1+dis2)/2)
   
    diss.append(dis3)
import operator
index, value = max(enumerate(diss), key=operator.itemgetter(1))

#print(value)



if(value>0.01):
    print(data['ans'][index])
    
else:
    print('please ask another question')    
    

#print(tok11)    