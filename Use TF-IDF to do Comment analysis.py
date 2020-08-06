#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import nltk as t
from sklearn.feature_extraction.text import TfidfVectorizer
file=['radpowerbikes','raldey','urbanbikedirect','aventon']
relationship=['father','mother','grandfather','grandmother','granddaughter',
              'grandson','son','daughter','parents','wife','husband','girlfriend','boyfriend']
stop_words=open('/Users/Ingridyuym/Desktop/comments/Sentiment-Lexicon-master/stopword.txt').read().replace('\n', ' ').split()
for i in file:
    name=i
    data=pd.read_excel('/Users/Ingridyuym/Desktop/e-bike/'+name+' comment.xlsx')
    new=data['comment']
    tf = TfidfVectorizer(stop_words=stop_words)
    tfidf_matrix = tf.fit_transform(new)
    word=tf.vocabulary_
    word=pd.DataFrame.from_dict(word,orient='index')
    word.to_excel('/Users/Ingridyuym/Desktop/e-bike/'+name+' comment analysis.xlsx')


# In[ ]:


for i in file:
    comment=[] 
    name=i
    data=pd.read_excel('/Users/Ingridyuym/Desktop/e-bike/'+name+' comment.xlsx')
    new=data['comment']
    for index, row in new.iteritems():
        each=t.word_tokenize(row)
        for e in each:
            if e in relationship:
                review=row
                comment.append(review)
                analysis=pd.DataFrame({'review':comment})
                analysis.to_excel('/Users/Ingridyuym/Desktop/e-bike/Demographics/'+name+' demographics analysis.xlsx',index=False)
            

