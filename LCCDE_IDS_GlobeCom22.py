#!/usr/bin/env python
# coding: utf-8

# # LCCDE: A Decision-Based Ensemble Framework for Intrusion Detection in The Internet of Vehicles
# This is the code for the paper entitled "**LCCDE: A Decision-Based Ensemble Framework for Intrusion Detection in The Internet of Vehicles**" accepted in 2022 IEEE Global Communications Conference (GLOBECOM).  
# Authors: Li Yang (lyang339@uwo.ca), Abdallah Shami (Abdallah.Shami@uwo.ca), Gary Stevens, and Stephen de Rusett  
# Organization: The Optimized Computing and Communications (OC2) Lab, ECE Department, Western University, Ontario, Canada; S2E Technologies, St. Jacobs, Ontario, Canada  
# 
# If you find this repository useful in your research, please cite:  
# L. Yang, A. Shami, G. Stevens, and S. DeRusett, “LCCDE: A Decision-Based Ensemble Framework for Intrusion Detection in The Internet of Vehicles," in 2022 IEEE Global Communications Conference (GLOBECOM), 2022, pp. 1-6.

# ## Import libraries

# In[1]:


import warnings
warnings.filterwarnings("ignore")


# In[2]:

import requests # for get requests
import json # to handle json requests from api endpoint

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score, precision_score, recall_score, f1_score
import lightgbm as lgb
import catboost as cbt
import xgboost as xgb
import time
from river import stream
from statistics import mode


# ## Read the sampled CICIDS2017 dataset
# The CICIDS2017 dataset is publicly available at: https://www.unb.ca/cic/datasets/ids-2017.html  
# Due to the large size of this dataset, the sampled subsets of CICIDS2017 is used. The subsets are in the "data" folder.  
# If you want to use this code on other datasets (e.g., CAN-intrusion dataset), just change the dataset name and follow the same steps. The models in this code are generic models that can be used in any intrusion detection/network traffic datasets.

# In[3]:


df = pd.read_csv("./data/CICIDS2017_sample_km.csv")


# In[4]:


df.Label.value_counts()


# **Corresponding Attack Types:**  
# 0 BENIGN &emsp; 18225  
# 3 DoS        &emsp;   &emsp;   3042  
# 6 WebAttack    &emsp;      2180  
# 1 Bot        &emsp;  &emsp;      1966    
# 5 PortScan  &emsp;       1255  
# 2 BruteForce  &emsp;      96  
# 4 Infiltration  &emsp;       36  

# ## Split train set and test set

# In[5]:


X = df.drop(['Label'],axis=1)
y = df['Label']
X_train, X_test, y_train, y_test = train_test_split(X,y, train_size = 0.8, test_size = 0.2, random_state = 0) #shuffle=False


# ## SMOTE to solve class-imbalance

# In[6]:


pd.Series(y_train).value_counts()


# In[7]:


from imblearn.over_sampling import SMOTE
smote=SMOTE(n_jobs=-1,sampling_strategy={2:1000,4:1000})


# In[8]:


X_train, y_train = smote.fit_resample(X_train, y_train)


# In[9]:


pd.Series(y_train).value_counts()


# ## Machine Learning (ML) model training
# ### Training three base learners: LightGBM, XGBoost, CatBoost

# In[10]:


# get_ipython().run_cell_magic('time', '', '# Train the LightGBM algorithm\nimport lightgbm as lgb\nlg = lgb.LGBMClassifier()\nlg.fit(X_train, y_train)\ny_pred = lg.predict(X_test)\nprint(classification_report(y_test,y_pred))\nprint("Accuracy of LightGBM: "+ str(accuracy_score(y_test, y_pred)))\nprint("Precision of LightGBM: "+ str(precision_score(y_test, y_pred, average=\'weighted\')))\nprint("Recall of LightGBM: "+ str(recall_score(y_test, y_pred, average=\'weighted\')))\nprint("Average F1 of LightGBM: "+ str(f1_score(y_test, y_pred, average=\'weighted\')))\nprint("F1 of LightGBM for each type of attack: "+ str(f1_score(y_test, y_pred, average=None)))\nlg_f1=f1_score(y_test, y_pred, average=None)\n\n# Plot the confusion matrix\ncm=confusion_matrix(y_test,y_pred)\nf,ax=plt.subplots(figsize=(5,5))\nsns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)\nplt.xlabel("y_pred")\nplt.ylabel("y_true")\nplt.show()\n')

import time
import lightgbm as lgb
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import json


def getinputs():    
    try:
        # Make a GET request to the endpoint
        response = requests.get('http://127.0.0.1:5000/fetch-data/lccde')
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # If successful, return the JSON data
            return response.json()
        else:
            # If not successful, print an error message
            print("Error:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        print("Exception:", e)
        return None

print('RESPONSES ON HERE: ' + json.dumps(getinputs()))

lgbm_ins = getinputs()
values = lgbm_ins['inputlist'] # for loop

# Start timing
start_time = time.time()
# Train the LightGBM algorithm
lg = lgb.LGBMClassifier()
lg.fit(X_train, y_train)
y_pred = lg.predict(X_test)
print(classification_report(y_test,y_pred))
print("Accuracy of LightGBM: "+ str(accuracy_score(y_test, y_pred)))
print("Precision of LightGBM: "+ str(precision_score(y_test, y_pred, average='weighted')))
print("Recall of LightGBM: "+ str(recall_score(y_test, y_pred, average='weighted')))
print("Average F1 of LightGBM: "+ str(f1_score(y_test, y_pred, average='weighted')))
print("F1 of LightGBM for each type of attack: "+ str(f1_score(y_test, y_pred, average=None)))
lg_f1=f1_score(y_test, y_pred, average=None)

classification_rep = classification_report(y_test,y_pred, output_dict=True)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
avg_f1 = f1_score(y_test, y_pred, average='weighted')
f1_per_class = f1_score(y_test, y_pred, average=None)

# Plot the confusion matrix
cm=confusion_matrix(y_test,y_pred)
f,ax=plt.subplots(figsize=(5,5))
sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.savefig("heatmaps/lightGBM.png")
# plt.show()

result_dict = {
    'classification_report': classification_rep,
    'accuracy': accuracy,
    'precision': precision,
    'recall': recall,
    'avg_f1': avg_f1,
    'f1_per_class': f1_per_class.tolist()  # Convert numpy array to list
}

with open('LightGBM_result.json', 'w') as json_file:
    json.dump(result_dict, json_file)

# End timing and print elapsed time
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")


# In[11]:


# get_ipython().run_cell_magic('time', '', '# Train the XGBoost algorithm\nimport xgboost as xgb\nxg = xgb.XGBClassifier()\n\nX_train_x = X_train.values\nX_test_x = X_test.values\n\nxg.fit(X_train_x, y_train)\n\ny_pred = xg.predict(X_test_x)\nprint(classification_report(y_test,y_pred))\nprint("Accuracy of XGBoost: "+ str(accuracy_score(y_test, y_pred)))\nprint("Precision of XGBoost: "+ str(precision_score(y_test, y_pred, average=\'weighted\')))\nprint("Recall of XGBoost: "+ str(recall_score(y_test, y_pred, average=\'weighted\')))\nprint("Average F1 of XGBoost: "+ str(f1_score(y_test, y_pred, average=\'weighted\')))\nprint("F1 of XGBoost for each type of attack: "+ str(f1_score(y_test, y_pred, average=None)))\nxg_f1=f1_score(y_test, y_pred, average=None)\n\n# Plot the confusion matrix\ncm=confusion_matrix(y_test,y_pred)\nf,ax=plt.subplots(figsize=(5,5))\nsns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)\nplt.xlabel("y_pred")\nplt.ylabel("y_true")\nplt.show()\n')

import time
import xgboost as xgb
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Start timing
start_time = time.time()

# Train the XGBoost algorithm
xg = xgb.XGBClassifier()

X_train_x = X_train.values
X_test_x = X_test.values

xg.fit(X_train_x, y_train)

y_pred = xg.predict(X_test_x)
print(classification_report(y_test,y_pred))
print("Accuracy of XGBoost: "+ str(accuracy_score(y_test, y_pred)))
print("Precision of XGBoost: "+ str(precision_score(y_test, y_pred, average='weighted')))
print("Recall of XGBoost: "+ str(recall_score(y_test, y_pred, average='weighted')))
print("Average F1 of XGBoost: "+ str(f1_score(y_test, y_pred, average='weighted')))
print("F1 of XGBoost for each type of attack: "+ str(f1_score(y_test, y_pred, average=None)))
xg_f1=f1_score(y_test, y_pred, average=None)

# Plot the confusion matrix
cm=confusion_matrix(y_test,y_pred)
f,ax=plt.subplots(figsize=(5,5))
sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.savefig("heatmaps/XGBoost.png")
# plt.show()

# End timing and print elapsed time
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")


# In[12]:


# get_ipython().run_cell_magic('time', '', '# Train the CatBoost algorithm\nimport catboost as cbt\ncb = cbt.CatBoostClassifier(verbose=0,boosting_type=\'Plain\')\n#cb = cbt.CatBoostClassifier()\n\ncb.fit(X_train, y_train)\ny_pred = cb.predict(X_test)\nprint(classification_report(y_test,y_pred))\nprint("Accuracy of CatBoost: "+ str(accuracy_score(y_test, y_pred)))\nprint("Precision of CatBoost: "+ str(precision_score(y_test, y_pred, average=\'weighted\')))\nprint("Recall of CatBoost: "+ str(recall_score(y_test, y_pred, average=\'weighted\')))\nprint("Average F1 of CatBoost: "+ str(f1_score(y_test, y_pred, average=\'weighted\')))\nprint("F1 of CatBoost for each type of attack: "+ str(f1_score(y_test, y_pred, average=None)))\ncb_f1=f1_score(y_test, y_pred, average=None)\n\n# Plot the confusion matrix\ncm=confusion_matrix(y_test,y_pred)\nf,ax=plt.subplots(figsize=(5,5))\nsns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)\nplt.xlabel("y_pred")\nplt.ylabel("y_true")\nplt.show()\n')

import time
import catboost as cbt
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Start timing
start_time = time.time()

# Train the CatBoost algorithm
cb = cbt.CatBoostClassifier(verbose=0, boosting_type='Plain')
#cb = cbt.CatBoostClassifier()

cb.fit(X_train, y_train)
y_pred = cb.predict(X_test)
print(classification_report(y_test,y_pred))
print("Accuracy of CatBoost: "+ str(accuracy_score(y_test, y_pred)))
print("Precision of CatBoost: "+ str(precision_score(y_test, y_pred, average='weighted')))
print("Recall of CatBoost: "+ str(recall_score(y_test, y_pred, average='weighted')))
print("Average F1 of CatBoost: "+ str(f1_score(y_test, y_pred, average='weighted')))
print("F1 of CatBoost for each type of attack: "+ str(f1_score(y_test, y_pred, average=None)))
cb_f1=f1_score(y_test, y_pred, average=None)

# Plot the confusion matrix
cm=confusion_matrix(y_test,y_pred)
f,ax=plt.subplots(figsize=(5,5))
sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.savefig("heatmaps/CatBoost.png")
# plt.show()s

# End timing and print elapsed time
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")


# ## Proposed ensemble model: Leader Class and Confidence Decision Ensemble (LCCDE)

# LCCDE aims to achieve optimal model performance by identifying the best-performing base ML model with the highest prediction confidence for each class. 

# ### Find the best-performing (leading) model for each type of attack among the three ML models

# In[13]:


# Leading model list for each class
model=[]
for i in range(len(lg_f1)):
    if max(lg_f1[i],xg_f1[i],cb_f1[i]) == lg_f1[i]:
        model.append(lg)
    elif max(lg_f1[i],xg_f1[i],cb_f1[i]) == xg_f1[i]:
        model.append(xg)
    else:
        model.append(cb)


# In[14]:


model


# **Leading Model for Each Type of Attack:**  
# 0 BENIGN: &emsp; XGBClassifier  
# 1 Bot:        &emsp;  &emsp;      XGBClassifier   
# 2 BruteForce:  &emsp;      LGBMClassifier  
# 3 DoS:        &emsp;   &emsp;   XGBClassifier  
# 4 Infiltration:  &emsp;       LGBMClassifier  
# 5 PortScan:  &emsp;       LGBMClassifier  
# 6 WebAttack:    &emsp;      XGBClassifier  

# ## LCCDE Prediction

# In[15]:


def LCCDE(X_test, y_test, m1, m2, m3):
    i = 0
    t = []
    m = []
    yt = []
    yp = []
    l = []
    pred_l = []
    pro_l = []

    # For each class (normal or a type of attack), find the leader model
    for xi, yi in stream.iter_pandas(X_test, y_test):

        xi2=np.array(list(xi.values()))
        y_pred1 = m1.predict(xi2.reshape(1, -1))      # model 1 (LightGBM) makes a prediction on text sample xi
        y_pred1 = int(y_pred1[0])
        y_pred2 = m2.predict(xi2.reshape(1, -1))      # model 2 (XGBoost) makes a prediction on text sample xi
        y_pred2 = int(y_pred2[0])
        y_pred3 = m3.predict(xi2.reshape(1, -1))      # model 3 (Catboost) makes a prediction on text sample xi
        y_pred3 = int(y_pred3[0])

        p1 = m1.predict_proba(xi2.reshape(1, -1))     # The prediction probability (confidence) list of model 1 
        p2 = m2.predict_proba(xi2.reshape(1, -1))     # The prediction probability (confidence) list of model 2  
        p3 = m3.predict_proba(xi2.reshape(1, -1))     # The prediction probability (confidence) list of model 3  

        # Find the highest prediction probability among all classes for each ML model
        y_pred_p1 = np.max(p1)
        y_pred_p2 = np.max(p2)
        y_pred_p3 = np.max(p3)

        if y_pred1 == y_pred2 == y_pred3: # If the predicted classes of all the three models are the same
            y_pred = y_pred1 # Use this predicted class as the final predicted class

        elif y_pred1 != y_pred2 != y_pred3: # If the predicted classes of all the three models are different
            # For each prediction model, check if the predicted class’s original ML model is the same as its leader model
            if model[y_pred1]==m1: # If they are the same and the leading model is model 1 (LightGBM)
                l.append(m1)
                pred_l.append(y_pred1) # Save the predicted class
                pro_l.append(y_pred_p1) # Save the confidence

            if model[y_pred2]==m2: # If they are the same and the leading model is model 2 (XGBoost)
                l.append(m2)
                pred_l.append(y_pred2)
                pro_l.append(y_pred_p2)

            if model[y_pred3]==m3: # If they are the same and the leading model is model 3 (CatBoost)
                l.append(m3)
                pred_l.append(y_pred3)
                pro_l.append(y_pred_p3)

            if len(l)==0: # Avoid empty probability list
                pro_l=[y_pred_p1,y_pred_p2,y_pred_p3]

            elif len(l)==1: # If only one pair of the original model and the leader model for each predicted class is the same
                y_pred=pred_l[0] # Use the predicted class of the leader model as the final prediction class

            else: # If no pair or multiple pairs of the original prediction model and the leader model for each predicted class are the same
                max_p = max(pro_l) # Find the highest confidence
                
                # Use the predicted class with the highest confidence as the final prediction class
                if max_p == y_pred_p1:
                    y_pred = y_pred1
                elif max_p == y_pred_p2:
                    y_pred = y_pred2
                else:
                    y_pred = y_pred3  
        
        else: # If two predicted classes are the same and the other one is different
            n = mode([y_pred1,y_pred2,y_pred3]) # Find the predicted class with the majority vote
            y_pred = model[n].predict(xi2.reshape(1, -1)) # Use the predicted class of the leader model as the final prediction class
            y_pred = int(y_pred[0]) 

        yt.append(yi)
        yp.append(y_pred) # Save the predicted classes for all tested samples
    return yt, yp


# In[16]:


#get_ipython().run_cell_magic('time', '', '# Implementing LCCDE\nyt, yp = LCCDE(X_test, y_test, m1 = lg, m2 = xg, m3 = cb)\n')

import time

# Start timing
start_time = time.time()

# Implementing LCCDE
yt, yp = LCCDE(X_test, y_test, m1=lg, m2=xg, m3=cb)

# End timing and print elapsed time
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")


# In[17]:


# The performance of the proposed lCCDE model
print("Accuracy of LCCDE: "+ str(accuracy_score(yt, yp)))
print("Precision of LCCDE: "+ str(precision_score(yt, yp, average='weighted')))
print("Recall of LCCDE: "+ str(recall_score(yt, yp, average='weighted')))
print("Average F1 of LCCDE: "+ str(f1_score(yt, yp, average='weighted')))
print("F1 of LCCDE for each type of attack: "+ str(f1_score(yt, yp, average=None)))


# In[18]:


# Comparison: The F1-scores for each base model
print("F1 of LightGBM for each type of attack: "+ str(lg_f1))
print("F1 of XGBoost for each type of attack: "+ str(xg_f1))
print("F1 of CatBoost for each type of attack: "+ str(cb_f1))


# **Conclusion**: The performance (F1-score) of the proposed LCCDE ensemble model on each type of attack detection is higher than any base ML model.

# In[ ]:




