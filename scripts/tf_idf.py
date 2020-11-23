import pandas as pd
import argparse
import json
import random
import re

def load_json(fname):
    content=[]
    with open(fname, 'r') as content_file:
        for jsonObj in content_file:
            Dict = json.loads(jsonObj)
            content.append(Dict)
    return content

def get_posts(content,num,maxlen):
    names=[]
    titles=[]
    coding=['']*num

    index=random.sample(range(maxlen),num)

    for i in index:
        names.append(content[i]['name'])
        titles.append(content[i]['title'])

    dic={"Name":names,"title":titles,"coding":coding}

    posts=pd.DataFrame(dic)

    return posts

def computeIDF(documents):
    import math
    N = len(documents)

    idfDict = dict.fromkeys(documents[0].keys(), 0)
    for document in documents:
        for word, val in document.items():
            if val > 0:
                idfDict[word] += 1

    for word, val in idfDict.items():
        idfDict[word] = math.log(N / float(val))
    return idfDict

def main():
        #load and random select 33 r/conservative posts from each day
    posts20_conserv=load_json("../data/trimmed_conservative_20112020.json")
    posts21_conserv=load_json("../data/trimmed_conservative_21112020.json")
    posts22_conserv=load_json("../data/trimmed_conservative_22112020.json")

    posts_1=get_posts(posts20_conserv,len(posts20_conserv),len(posts20_conserv))
    posts_2=get_posts(posts21_conserv,len(posts21_conserv),len(posts21_conserv))
    posts_3=get_posts(posts22_conserv,len(posts22_conserv),len(posts22_conserv))

    #load and random select 33 r/politics posts from each day
    posts20_politics=load_json("../data/trimmed_politics_20112020.json")
    posts21_politics=load_json("../data/trimmed_politics_21112020.json")
    posts22_politics=load_json("../data/trimmed_politics_22112020.json")

    posts_4=get_posts(posts20_politics,len(posts20_politics),len(posts20_politics))
    posts_5=get_posts(posts21_politics,len(posts21_politics),len(posts21_politics))
    posts_6=get_posts(posts22_politics,len(posts22_politics),len(posts22_politics))

    pdList = []
    pdList.extend(value for name, value in locals().items() if name.startswith('posts_'))
    result=pd.concat(pdList)

    title_list=list(result['title'])

    word_bag=[]
    for doc in title_list:
        for match in re.finditer(r'[^.,?!\s]+|[.,?!]', doc):
            word_bag.append(match.group())

    uniqueWords = set(word_bag)
    numOfWords= dict.fromkeys(uniqueWords, 0)
    for word in word_bag:
        numOfWords[word] += 1
    #TODO: IDF showing all 0
    IDF=computeIDF([numOfWords])

if __name__=='__main__':
    main()
