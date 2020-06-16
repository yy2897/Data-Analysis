#!/usr/bin/env python
# coding: utf-8

# In[110]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os 

#read file
tb=pd.read_csv('/Users/Ingridyuym/Downloads/tb.csv')
#get all the columns
tb.columns.values.tolist()
#drop unessary columns
tb.drop(['m04','m514','m014','f04','f514','f014'],axis=1,inplace=True)
#unpivot
df=tb.melt(id_vars=['country','year'],var_name='v',value_name='cases')
#drop na
df=df.dropna()
#extract data to create new colunms: sex and age
df['sex']=df.v.str[0]
df['age']=df.v.str[1:].str[0:2]+'-'+df.v.str[1:].str[2:4]
#delete old colums
df=df.drop(['v'],axis=1)
#reorder the columns
order=['country','year','age','sex','cases']
df=df[order]
#sort the value
df=df.sort_values(by=['country','year','age','sex'])
#create clean dataset file without index
df.to_csv('/Users/Ingridyuym/Downloads/finaldataset.csv',index=False)

