#!/usr/bin/env python
# coding: utf-8

#  #  <p style="text-align: center;">Discovering customer attrition patterns</p> 

# I analyze customer attrition data to discover patterns. These will help the marketing team to dive deeper into those patterns and do root cause analysis of why they are happening. I will use association rules mining algorithm for this purpose.

# ## Load the Dataset and Transform
# 
# 

# In[1]:


from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os
import matplotlib.pylab as plt
from apyori import apriori

#Load the prospect dataset
raw_data = pd.read_csv("attrition.csv")

raw_data.head()


# In[3]:




basket_str = ""
for rowNum, row in raw_data.iterrows():
    
    #Break lines
    if (rowNum != 0):
        basket_str = basket_str + "\n"
    #Add the rowid as the first column
    basket_str = basket_str + str(rowNum) 
    #Add columns
    for colName, col in row.iteritems():
        basket_str = basket_str + ",\"" + colName + "=" + str(col) +"\""

#print(basket_str)
basket_file=open("warranty_basket.csv","w")
basket_file.write(basket_str)
basket_file.close()


# ## Build Association Rules
# 
# Use the apriori algorithm to build association rules. Then extract the results and populate a data frame for future use. The apriori provides the LHS for multiple combinations of the items. I capture the counts along with confidence and lift in this example

# In[10]:


#read back
basket_data=pd.read_csv("warranty_basket.csv",header=None)
filt_data = basket_data.drop(basket_data.columns[[0]], axis=1)
results= list(apriori(filt_data.values.tolist(),min_support=0.3))
print(results)
rulesList= pd.DataFrame(columns=('LHS', 'RHS', 'COUNT', 'CONFIDENCE','LIFT'))
rowCount=0

for row in results:
    for affinity in row[2]:
        rulesList.loc[rowCount] = [ ', '.join(affinity.items_base) ,                                    affinity.items_add,                                     len(affinity.items_base) ,                                    affinity.confidence,                                    affinity.lift]
        rowCount +=1



# ## Using the Rules

# In[11]:


rulesList.head()


# We can also filter rules where the count of elements is 1 and the confidence is > 70%

# In[12]:


rulesList[(rulesList.COUNT <= 1) & (rulesList.CONFIDENCE > 0.7)].head(5)


# Looking at the rules, we can easily see some patterns. Customers who have left the business between 1 year and 2 years are always in the age group 30-50. Similarly, customers in age group 20-30 always cancelled the service. These are interesting facts that can be analyzed further by the business.
