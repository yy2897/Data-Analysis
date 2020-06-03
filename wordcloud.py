#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
from PIL import Image
import numpy as np

from lxml import etree
from ipykernel import kernelapp as app

data = pd.read_csv('./Department_Information-1.csv')
data= data['Department_Name']
data.to_csv('./Department_Information.csv',index=None)
content=(open('Department_Information.csv')).read()
cutdata=jieba.cut(content)
cut_text = " ".join(cutdata)
def remove_stop_words(f):
    stop_words = ['Engineering', 'Science', '&', ' Centre', 'for', '(', ')', 'School', 'Teaching', 'Design', 'National','Research' ]
    for stop_word in stop_words:
       f = f.replace(stop_word, '')
    return f
cut=remove_stop_words(cut_text)
img = Image.open('788px-Love_Heart_symbol.svg.png') 
img_array = np.array(img)
wc = WordCloud( max_words=100, width=2000, height=1200 )
print(cut) 
wordcloud = wc.generate(cut)
wordcloud.to_file("wordcloud.jpg")
plt.imshow(wordcloud)

