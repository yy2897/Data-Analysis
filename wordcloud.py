#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
from PIL import Image
import numpy as np

#read data
data = pd.read_csv('./Department_Information-1.csv')
data= data['Department_Name']
#extract department data from the dataset 
data.to_csv('./Department_Information.csv',index=None)
content=(open('Department_Information.csv')).read()
#cut the word
cutdata=jieba.cut(content)
cut_text = " ".join(cutdata)
#define the function 'remove_stop_words' to remove the meaningless words such as '&','centre' etc.
def remove_stop_words(f):
    stop_words = ['Engineering', 'Science', '&', ' Centre', 'for', '(', ')', 'School', 'Teaching', 'Design', 'National','Research' ]
    for stop_word in stop_words:
       f = f.replace(stop_word, '')
    return f
#remove meaningless words 
cut=remove_stop_words(cut_text)
#load the image for the shape of the wordcloud
img = Image.open('111.jpg') 
img_array = np.array(img)
#the wordcloud format
wc = WordCloud( background_color='white',width=4000, height=1200,mask=img_array)
wordcloud = wc.generate(cut)
#generate wordcloud
wordcloud.to_file("wordcloud.jpg")
wc.generate_from_text(cut)
plt.imshow(wordcloud)

