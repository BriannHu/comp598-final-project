import pandas as pd
import argparse
import json
import random
import math
import numpy as np

def cal_idf_p(b):
    N=8 #TODO: the total number of topics
    wordsUnique=[]
    topics_wordset={ key: set(b[key].keys()) for key in b }
    for dic in list(b.values()):
        wordsUnique.extend(dic.keys())
    wordsUnique=set(wordsUnique)
    idf={key:0 for key in wordsUnique}


    for topic in b:
        for word in b[topic].keys():
            idf[word]+=1
    for word in idf:
        idf[word]=math.log(N/idf[word])

    return idf

def tfidf(b,idf):
    tfidfs=dict.fromkeys(b)
    for topic in tfidfs:
        tfidf={}
        for topic in b[topic].keys():
            tfidf[word]=b[pony][word] * idf[word]
        tfidfs[pony]=tfidf
    return tfidfs


topics=list(set(newb['coding']))
topics =[x for x in topics if str(x) != 'nan']


def get_dialogs(df):
    #this function return a dictionary with value of lists of words
    result={}
    for topic in topics:
        temp=df[df['coding']==topic]['title']
        out = ' '.join(temp.astype(str))
        out=re.sub("\<U\+[0-9]{4}\>"," ",out)
        to_delete = "'~`@$%^*_+={}|\"/<>"

        words=re.sub(r'[^\w'+to_delete+']', " ",out).split()

        words=[word.lower() for word in words if (word.isalpha())]
        result[topic]=words
    return result

def counts(dialogs):
    result=dict.fromkeys(dialogs)
    for topic in list(dialogs.keys()):
        list_of_words=dialogs[topic]
        wordsUnique=set(list_of_words)

        count={key:0 for key in wordsUnique}
        for word in list_of_words:
            count[word]+=1
        for word in list(count.keys()):
            if count[word]<5:
                del count[word]
        result[topic]=count
    return result

def take_top_n(tfidf,num):
    top={}
    for pony in tfidf:
        x=tfidf[pony]
        top[pony]=list(dict(sorted(x.items(), key=lambda item: item[1],reverse=True)[:num]).keys())
    return top

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('csv',help='the csv file')
    parser.add_argument('out_num',help='number of output you want.')

    args=parser.parse_args()
    newb=pd.read_csv(args.csv)
    dialog=get_dialogs(newb[newb['coding'].notna()])
    b=counts(dialog)
    newidf=cal_idf_p(b)
    newtfidf=tfidf(b,newidf)
    print(take_top_n(newtfidf,args.out_num))
    return
if __name__=='__main__':
    main()
