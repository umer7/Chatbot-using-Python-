# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 18:10:22 2018

@author: spy
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 21:36:56 2018

@author: umer
"""
from flask import Flask
from flask import request
import os
from urllib import parse

#from psycopg2 import sql
import re, math
from textblob import TextBlob
from collections import Counter
import operator


app = Flask(__name__)


@app.route('/')
def use():
    try:
        conn = psycopg2.connect("dbname='db1' user='postgres' password='umer'")
        print("sucessfull")
    except:
        print("failed")
    return 'Hello World!'

@app.route('/postjson', methods = ['POST'])
def postJsonHandler():
    print (request.is_json)
    content = request.get_json()
    print(type(content))
    print(content['device'])
    try:
        conn = psycopg2.connect("dbname='db1' user='postgres' password='umer'")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS qa11 ( qa text);")
        cur.execute(sql.SQL("insert into {} values (%s)").format(sql.Identifier('qa11')), [content['device']])
        print("inset")
    except:
        print("failed")
    #print (content)
    return '12'

@app.route('/store_query', methods=['GET', 'POST'])
def query1():
    print(request.is_json)
    dictq = request.get_json()
    conn = psycopg2.connect("dbname='db1' user='postgres' password='umer'")
    cur = conn.cursor()
    t1="hy"
    t2="k"
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS query ( qid INT ,query TEXT,botid INT );")

        print("query created")
    except:
        print("query failed")
    try:

        cur.execute(sql.SQL("insert into {} values (%s,%s,%s)").format(sql.Identifier('query')),[dictq['qid'],dictq['query'],dictq['botid']])
        cur.execute("SELECT * FROM query ;")
        print(cur.fetchone())
        print("success2")
    except:
        print("failed")
    cur.execute("commit;")
    return dictq['botid']
#    return 'question is  %s' % question

@app.route('/store_response', methods=['GET', 'POST'])
def response():
    print(request.is_json)
    dictr = request.get_json()
    conn = psycopg2.connect("dbname='db1' user='postgres' password='umer'")
    cur = conn.cursor()
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS response ( rid INT ,response text,qid INT);")
        print("response created")
    except:
        print("response failed")
    try:
        cur.execute(sql.SQL("insert into {} values (%s,%s,%s)").format(sql.Identifier('response')),[dictr['rid'],dictr['response'],dictr['qid']])
        cur.execute("SELECT * FROM response ;")
        print(cur.fetchone())
        print("success2")
    except:
        print("failed")
    cur.execute("commit;")
    return dictr['qid']

    #cur.execute(sql.SQL("insert into {} values (%s)").format(sql.Identifier('response')),[answer])
    #return 'answer is  %s' % answer

@app.route('/get_response/<query>', methods=['GET', 'POST'])
def query(query):
    conn = psycopg2.connect("dbname='db1' user='postgres' password='umer'")
    cur = conn.cursor()
    botid1=21
    query="helooo"
    try:
        cur.execute("SELECT query FROM query WHERE botid=%s ;", [botid1])
        l1=cur.fetchall()
        #print(l1)
        len1=len(l1)
        #print(len(l1))

        #print("response suceed3")
    except:
        print(" response failed3")
    """try:
        cur.execute("SELECT * FROM query ;")
        print(cur.fetchall())
        print("query suceed3")
    except:
        print(" query failed3")"""

    #cur.execute("SELECT * FROM qa11 ;")
    #cur.execute("CREATE TABLE IF NOT EXISTS qa11 ( qa text);")
    #print(cur.fetchone())
    text1 = 'I like cat'
    #text2 = 'I liikee dog'
    text2=remove_spell_errors(query)
    diss = []
    print((str(l1[1])))
#    str1 = ','.remove(str(l1[1]))


    #str1 = str(l1[1]).replace(")", "")
    #str1=str(l1[1]).replace(",","").replace("(","").replace("'", "").replace(")", "")
    #str1 = str1.replace("'", "")
    for j in range(0,len1):
        print(l1[j])
        l1[j]=str(l1[1]).replace(",","").replace("(","").replace("'", "").replace(")", "")
        print(l1[j])
        print("\n")
    #print(str1)

    #print(float(get_cosine(str(11[0]), str(query))))
    try:
        for i in range(0,len1):
            print("lop")
            #print(l1[i])
            #dis1 = float(get_cosine(str(11[i]), str(query)))
            #print(dis1)
            #diss.append(dis1)

 #       dis1=float(get_cosine(str(text1),str(text2)))
        #print(diss)
    except:
        print("cosine failed")
    try:
        dis2=float(DistJaccard(str(text1),str(text2)))
        #print(dis2)
    except:
        print("jack failed")
    return 'query is  %s' % text2



WORD = re.compile(r'\w+')
def get_cosine(vec1, vec2):
    vec1 = Counter(WORD.findall(vec1))
    vec2 = Counter(WORD.findall(vec2))
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
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

def remove_spell_errors(text):
    b = TextBlob(text)
    return b.correct()



if __name__ == '__main__':
    app.run()
