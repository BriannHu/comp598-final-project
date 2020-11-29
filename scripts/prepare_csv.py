import pandas as pd
import json
import random
import numpy as np

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
def main():
    #load and random select 33 r/conservative posts from each day
    posts20_conserv=load_json("comp598-final-project/data/cleaned_conservative_20112020.json")
    posts21_conserv=load_json("comp598-final-project/data/cleaned_conservative_21112020.json")
    posts22_conserv=load_json("comp598-final-project/data/cleaned_conservative_22112020.json")

    posts_1=get_posts(posts20_conserv,len(posts20_conserv),len(posts20_conserv))
    posts_2=get_posts(posts21_conserv,len(posts21_conserv),len(posts21_conserv))
    posts_3=get_posts(posts22_conserv,len(posts22_conserv),len(posts22_conserv))

    #load and random select 33 r/politics posts from each day
    posts20_politics=load_json("comp598-final-project/data/cleaned_politics_20112020.json")
    posts21_politics=load_json("comp598-final-project/data/cleaned_politics_21112020.json")
    posts22_politics=load_json("comp598-final-project/data/cleaned_politics_22112020.json")

    posts_4=get_posts(posts20_politics,len(posts20_politics),len(posts20_politics))
    posts_5=get_posts(posts21_politics,len(posts21_politics),len(posts21_politics))
    posts_6=get_posts(posts22_politics,len(posts22_politics),len(posts22_politics))

    pdList = []
    pdList.extend(value for name, value in locals().items() if name.startswith('posts_'))
    result=pd.concat(pdList)
    unique_posts=result.drop_duplicates()
    ls=list(posts_1['Name'])
    ls.extend(posts_4['Name'])
    st=set(ls)
    remain=unique_posts[np.logical_not(unique_posts['Name'].isin(st))]
    dw=remain.head(258)
    dw.to_csv('comp598-final-project/data/posts_for_dawei.csv',index=False)
    lg=remain.tail(258)
    lg.to_csv('comp598-final-project/data/posts_for_logan.csv',index=False)
    return
if __name__ ='__main__':
    main()
