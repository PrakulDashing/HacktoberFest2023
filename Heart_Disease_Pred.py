#!/usr/bin/env python
# coding: utf-8

# In[21]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


# In[2]:


df = pd.read_csv('/Users/kirtan/Downloads/heart_1.csv')


# In[3]:


df.head()


# In[4]:


df.info()


# In[5]:


df.shape


# In[6]:


df.isnull().sum()


# # Data Visualization

# In[8]:


sns.pairplot(data=df, hue='target')
plt.show()


# In[11]:


plt.figure(figsize=(12,12))
sns.heatmap(df.corr(), cmap='jet', annot=True, linecolor='black', linewidths=0.5)
plt.show()


# In[13]:


sns.countplot(data=df, x='target')
plt.show()


# # Train & Test Split

# In[15]:


X = df.iloc[:,:-1]
X


# In[16]:


y = df['target']
y


# In[32]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)


# # Model

# In[33]:


RNF = RandomForestClassifier()


# In[34]:


RNF.fit(X_train, y_train)


# In[35]:


#Predictions
y_hat = RNF.predict(X_test)


# # Model Evaluation

# In[36]:


accuracy_score(y_test, y_hat)


# In[37]:


print(classification_report(y_test, y_hat))


# In[38]:


sns.heatmap(confusion_matrix(y_test, y_hat), annot=True, cmap='coolwarm', linecolor='black', linewidths=0.5)
plt.show()


# In[ ]:




