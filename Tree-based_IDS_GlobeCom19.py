#!/usr/bin/env python
# coding: utf-8

# # Tree-Based Intelligent Intrusion Detection System in Internet of Vehicles 
# This is the code for the paper entitled "[**Tree-Based Intelligent Intrusion Detection System in Internet of Vehicles**](https://arxiv.org/pdf/1910.08635.pdf)" published in IEEE GlobeCom 2019.  
# Authors: Li Yang (liyanghart@gmail.com), Abdallah Moubayed, Ismail Hamieh, and Abdallah Shami  
# Organization: The Optimized Computing and Communications (OC2) Lab, ECE Department, Western University
# 
# If you find this repository useful in your research, please cite:  
# L. Yang, A. Moubayed, I. Hamieh and A. Shami, "Tree-Based Intelligent Intrusion Detection System in Internet of Vehicles," 2019 IEEE Global Communications Conference (GLOBECOM), 2019, pp. 1-6, doi: 10.1109/GLOBECOM38437.2019.9013892.  

# ## Import libraries

# In[2]:


import warnings
warnings.filterwarnings("ignore")


# In[3]:

import requests # for get requests
import json # to handle json requests from api endpoint

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder 
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score,precision_recall_fscore_support
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestClassifier,ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb
from xgboost import plot_importance

def getinputs():    
    try:
        # Make a GET request to the endpoint
        response = requests.get('http://127.0.0.1:5000/fetch-data/tree')
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # If successful, return the JSON data
            return response.json()
        else:
            # If not successful, print an error message
            print("Error:", response.status_code)
            return {'model':{'input_list': None}}
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        print("Exception:", e)
        return {'model':{'input_list': None}}

# print('RESPONSES ON HERE: ' + json.dumps(getinputs()))

test = json.dumps(getinputs())
algorithm_data = json.loads(test)

print(f'Algorithm Data: {algorithm_data}')

ds = algorithm_data['dataset']
if ds == "":
    ds = "CICIDS2017_sample.csv"

if algorithm_data['random_state'] == '':
    rs = 0
else: 
    rs = int(algorithm_data['random_state'])

if algorithm_data['learning_rate'] == '':
    lr = None
else:
    lr = float(algorithm_data['learning_rate'])

if algorithm_data['n_estimator'] == '':
    ne = 10
else: 
    ne = int(algorithm_data['n_estimator'])

if algorithm_data['max_depth'] == '':
    md = None
else :
    md = int(algorithm_data['max_depth'])

if algorithm_data['max_feature'] == '':
    mf = None
else :
    mf = int(algorithm_data['max_feature'])

if algorithm_data['min_samples_split'] == '':
    mss = 0.1
else :
    mss = int(algorithm_data['min_samples_split'])

if algorithm_data['min_samples_leaf'] == '':
    msl = 0.1
else :
    msl = float(algorithm_data['min_samples_leaf'])

print(f'Algorithm Data: {algorithm_data}')
print(f'random_state: {rs}')
print(f'learning_rate: {lr}')
print(f'n_estimator: {ne}')
print(f'max_depth: {lr}')
print(f'max_feature: {mf}')
print(f'min_samples_split: {mss}')
print(f'min_samples_leaf: {msl}')


# ## Read the sampled CICIDS2017 dataset
# The CICIDS2017 dataset is publicly available at: https://www.unb.ca/cic/datasets/ids-2017.html  
# Due to the large size of this dataset, the sampled subsets of CICIDS2017 is used. The subsets are in the "data" folder.  
# If you want to use this code on other datasets (e.g., CAN-intrusion dataset), just change the dataset name and follow the same steps. The models in this code are generic models that can be used in any intrusion detection/network traffic datasets.

# # In[3]:


# #Read dataset
# df = pd.read_csv('./data/Monday-WorkingHours.pcap_ISCX.csv')
# # The results in this code is based on the original CICIDS2017 dataset. Please go to cell [10] if you work on the sampled dataset. 


# # In[ ]:


# df


# # In[ ]:


# df.Label.value_counts()


# # ### Data sampling
# # Due to the space limit of GitHub files, we sample a small-sized subset for model learning using random sampling

# # In[ ]:


# # Randomly sample instances from majority classes
# df_minor = df[(df['Label']=='WebAttack')|(df['Label']=='Bot')|(df['Label']=='Infiltration')]
# df_BENIGN = df[(df['Label']=='BENIGN')]
# df_BENIGN = df_BENIGN.sample(n=None, frac=0.01, replace=False, weights=None, random_state=None, axis=0)
# df_DoS = df[(df['Label']=='DoS')]
# df_DoS = df_DoS.sample(n=None, frac=0.05, replace=False, weights=None, random_state=None, axis=0)
# df_PortScan = df[(df['Label']=='PortScan')]
# df_PortScan = df_PortScan.sample(n=None, frac=0.05, replace=False, weights=None, random_state=None, axis=0)
# df_BruteForce = df[(df['Label']=='BruteForce')]
# df_BruteForce = df_BruteForce.sample(n=None, frac=0.2, replace=False, weights=None, random_state=None, axis=0)


# # In[ ]:


# df_s = df_BENIGN._append(df_DoS)._append(df_PortScan)._append(df_BruteForce)._append(df_minor)


# # In[ ]:


# df_s = df_s.sort_index()


# # In[ ]:


# # Save the sampled dataset
# df_s.to_csv('./data/CICIDS2017_sample.csv',index=0)


# # ### Preprocessing (normalization and padding values)

# In[4]:

dataset = "./data/" + ds
df = pd.read_csv(dataset)


# In[5]:


# Min-max normalization
numeric_features = df.dtypes[df.dtypes != 'object'].index
df[numeric_features] = df[numeric_features].apply(
    lambda x: (x - x.min()) / (x.max()-x.min()))
# Fill empty values by 0
df = df.fillna(0)


# ### split train set and test set

# In[6]:


labelencoder = LabelEncoder()
df.iloc[:, -1] = labelencoder.fit_transform(df.iloc[:, -1])
X = df.drop(['Label'],axis=1).values 
y = df.iloc[:, -1].values.reshape(-1,1)
y=np.ravel(y)
X_train, X_test, y_train, y_test = train_test_split(X,y, train_size = 0.8, test_size = 0.2, random_state = 0,stratify = y)


# In[7]:


X_train.shape


# In[8]:


pd.Series(y_train).value_counts()


# ### Oversampling by SMOTE

# In[9]:


from imblearn.over_sampling import SMOTE
smote=SMOTE(n_jobs=-1,sampling_strategy={4:1500}) # Create 1500 samples for the minority class "4"


# In[11]:


y_train =y_train.astype('int')
X_train, y_train = smote.fit_resample(X_train, y_train)


# In[12]:


pd.Series(y_train).value_counts()


# ## Machine learning model training

# ### Training four base learners: decision tree, random forest, extra trees, XGBoost

# In[13]:


# Decision tree training and prediction
y_test = y_test.astype('int')
dt = DecisionTreeClassifier(random_state = rs, max_depth=md, max_features=mf, min_samples_split=mss, min_samples_leaf=msl)
dt.fit(X_train,y_train) 
dt_score=dt.score(X_test,y_test)
y_predict=dt.predict(X_test)
y_true=y_test
print('Accuracy of DT: '+ str(dt_score))
precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted') 
print('Precision of DT: '+(str(precision)))
print('Recall of DT: '+(str(recall)))
print('F1-score of DT: '+(str(fscore)))
print(classification_report(y_true,y_predict))
cm=confusion_matrix(y_true,y_predict)
f,ax=plt.subplots(figsize=(5,5))
sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.savefig("heatmaps/TB_DecisionTree.png")
#plt.show()


# In[14]:


dt_train=dt.predict(X_train)
dt_test=dt.predict(X_test)


# In[15]:


# Random Forest training and prediction
rf = RandomForestClassifier(random_state = rs, max_depth=md, max_features=mf, min_samples_split=mss, min_samples_leaf=msl)
rf.fit(X_train,y_train) 
rf_score=rf.score(X_test,y_test)
y_predict=rf.predict(X_test)
y_true=y_test
print('Accuracy of RF: '+ str(rf_score))
precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted') 
print('Precision of RF: '+(str(precision)))
print('Recall of RF: '+(str(recall)))
print('F1-score of RF: '+(str(fscore)))
print(classification_report(y_true,y_predict))
cm=confusion_matrix(y_true,y_predict)
f,ax=plt.subplots(figsize=(5,5))
sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.savefig("heatmaps/TB_RandomForest.png")
#plt.show()


# In[16]:


rf_train=rf.predict(X_train)
rf_test=rf.predict(X_test)


# In[17]:


# Extra trees training and prediction
et = ExtraTreesClassifier(random_state = rs, max_depth=md, max_features=mf, min_samples_split=mss, min_samples_leaf=msl)
et.fit(X_train,y_train) 
et_score=et.score(X_test,y_test)
y_predict=et.predict(X_test)
y_true=y_test
print('Accuracy of ET: '+ str(et_score))
precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted') 
print('Precision of ET: '+(str(precision)))
print('Recall of ET: '+(str(recall)))
print('F1-score of ET: '+(str(fscore)))
print(classification_report(y_true,y_predict))
cm=confusion_matrix(y_true,y_predict)
f,ax=plt.subplots(figsize=(5,5))
sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.savefig("heatmaps/TB_ExtraTrees.png")
#plt.show()


# In[18]:


et_train=et.predict(X_train)
et_test=et.predict(X_test)


# In[19]:


# XGboost training and prediction
xg = xgb.XGBClassifier(n_estimators = ne, learning_rate=lr)
xg.fit(X_train,y_train)
xg_score=xg.score(X_test,y_test)
y_predict=xg.predict(X_test)
y_true=y_test
print('Accuracy of XGBoost: '+ str(xg_score))
precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted') 
print('Precision of XGBoost: '+(str(precision)))
print('Recall of XGBoost: '+(str(recall)))
print('F1-score of XGBoost: '+(str(fscore)))
print(classification_report(y_true,y_predict))
cm=confusion_matrix(y_true,y_predict)
f,ax=plt.subplots(figsize=(5,5))
sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.savefig("heatmaps/TB_XGB.png")
#plt.show()


# In[20]:


xg_train=xg.predict(X_train)
xg_test=xg.predict(X_test)


# ### Stacking model construction (ensemble for 4 base learners)

# In[21]:


# Use the outputs of 4 base models to construct a new ensemble model
base_predictions_train = pd.DataFrame( {
    'DecisionTree': dt_train.ravel(),
        'RandomForest': rf_train.ravel(),
     'ExtraTrees': et_train.ravel(),
     'XgBoost': xg_train.ravel(),
    })
base_predictions_train.head(5)


# In[22]:


dt_train=dt_train.reshape(-1, 1)
et_train=et_train.reshape(-1, 1)
rf_train=rf_train.reshape(-1, 1)
xg_train=xg_train.reshape(-1, 1)
dt_test=dt_test.reshape(-1, 1)
et_test=et_test.reshape(-1, 1)
rf_test=rf_test.reshape(-1, 1)
xg_test=xg_test.reshape(-1, 1)


# In[23]:


x_train = np.concatenate(( dt_train, et_train, rf_train, xg_train), axis=1)
x_test = np.concatenate(( dt_test, et_test, rf_test, xg_test), axis=1)


# In[24]:


stk = xgb.XGBClassifier().fit(x_train, y_train)


# In[25]:


y_predict=stk.predict(x_test)
y_true=y_test
stk_score=accuracy_score(y_true,y_predict)
print('Accuracy of Stacking: '+ str(stk_score))
precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted') 
print('Precision of Stacking: '+(str(precision)))
print('Recall of Stacking: '+(str(recall)))
print('F1-score of Stacking: '+(str(fscore)))
print(classification_report(y_true,y_predict))
cm=confusion_matrix(y_true,y_predict)
f,ax=plt.subplots(figsize=(5,5))
sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.savefig("heatmaps/TB_StackModel.png")
# plt.show()


# ## Feature Selection

# ### Feature importance

# In[26]:


# Save the feature importance lists generated by four tree-based algorithms
dt_feature = dt.feature_importances_
rf_feature = rf.feature_importances_
et_feature = et.feature_importances_
xgb_feature = xg.feature_importances_


# In[27]:


# calculate the average importance value of each feature
avg_feature = (dt_feature + rf_feature + et_feature + xgb_feature)/4


# In[28]:


feature=(df.drop(['Label'],axis=1)).columns.values
print ("Features sorted by their score:")
print (sorted(zip(map(lambda x: round(x, 4), avg_feature), feature), reverse=True))


# In[29]:


f_list = sorted(zip(map(lambda x: round(x, 4), avg_feature), feature), reverse=True)


# In[30]:


len(f_list)


# In[31]:


# Select the important features from top-importance to bottom-importance until the accumulated importance reaches 0.9 (out of 1)
Sum = 0
fs = []
for i in range(0, len(f_list)):
    Sum = Sum + f_list[i][0]
    fs.append(f_list[i][1])
    if Sum>=0.9:
        break        


# In[32]:


X_fs = df[fs].values


# In[33]:


X_train, X_test, y_train, y_test = train_test_split(X_fs,y, train_size = 0.8, test_size = 0.2, random_state = 0,stratify = y)


# In[34]:


X_train.shape


# In[35]:


pd.Series(y_train).value_counts()


# ### Oversampling by SMOTE

# In[36]:


from imblearn.over_sampling import SMOTE
smote=SMOTE(n_jobs=-1,sampling_strategy={4:1500})


# In[38]:


y_train =y_train.astype('int')
X_train, y_train = smote.fit_resample(X_train, y_train)


# In[39]:


pd.Series(y_train).value_counts()


# ## Machine learning model training after feature selection

# In[41]:


y_test = y_test.astype('int')
dt = DecisionTreeClassifier(random_state = rs, max_depth=md, max_features=mf, min_samples_split=mss, min_samples_leaf=msl)
dt.fit(X_train,y_train) 
dt_score=dt.score(X_test,y_test)
y_predict=dt.predict(X_test)
y_true=y_test
print('Accuracy of DT: '+ str(dt_score))
precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted') 
print('Precision of DT: '+(str(precision)))
print('Recall of DT: '+(str(recall)))
print('F1-score of DT: '+(str(fscore)))
print(classification_report(y_true,y_predict))
cm=confusion_matrix(y_true,y_predict)
f,ax=plt.subplots(figsize=(5,5))
sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.savefig("heatmaps/TB_FS_DecisionTree.png")
# plt.show()


# In[42]:


dt_train=dt.predict(X_train)
dt_test=dt.predict(X_test)


# In[43]:


rf = RandomForestClassifier(random_state = rs, max_depth=md, max_features=mf, min_samples_split=mss, min_samples_leaf=msl)
rf.fit(X_train,y_train) # modelin veri üzerinde öğrenmesi fit fonksiyonuyla yapılıyor
rf_score=rf.score(X_test,y_test)
y_predict=rf.predict(X_test)
y_true=y_test
print('Accuracy of RF: '+ str(rf_score))
precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted') 
print('Precision of RF: '+(str(precision)))
print('Recall of RF: '+(str(recall)))
print('F1-score of RF: '+(str(fscore)))
print(classification_report(y_true,y_predict))
cm=confusion_matrix(y_true,y_predict)
f,ax=plt.subplots(figsize=(5,5))
sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.savefig("heatmaps/TB_FS_RandomForest.png")
# plt.show()


# In[44]:


rf_train=rf.predict(X_train)
rf_test=rf.predict(X_test)


# In[45]:


et = ExtraTreesClassifier(random_state = rs, max_depth=md, max_features=mf, min_samples_split=mss, min_samples_leaf=msl)
et.fit(X_train,y_train) 
et_score=et.score(X_test,y_test)
y_predict=et.predict(X_test)
y_true=y_test
print('Accuracy of ET: '+ str(et_score))
precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted') 
print('Precision of ET: '+(str(precision)))
print('Recall of ET: '+(str(recall)))
print('F1-score of ET: '+(str(fscore)))
print(classification_report(y_true,y_predict))
cm=confusion_matrix(y_true,y_predict)
f,ax=plt.subplots(figsize=(5,5))
sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.savefig("heatmaps/TB_FS_ExtraTrees.png")
# plt.show()


# In[46]:


et_train=et.predict(X_train)
et_test=et.predict(X_test)


# In[47]:


xg = xgb.XGBClassifier(n_estimators = ne, learning_rate=lr)
xg.fit(X_train,y_train)
xg_score=xg.score(X_test,y_test)
y_predict=xg.predict(X_test)
y_true=y_test
print('Accuracy of XGBoost: '+ str(xg_score))
precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted') 
print('Precision of XGBoost: '+(str(precision)))
print('Recall of XGBoost: '+(str(recall)))
print('F1-score of XGBoost: '+(str(fscore)))
print(classification_report(y_true,y_predict))
cm=confusion_matrix(y_true,y_predict)
f,ax=plt.subplots(figsize=(5,5))
sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.savefig("heatmaps/TB_FS_XGB.png")
# plt.show()


# In[48]:


xg_train=xg.predict(X_train)
xg_test=xg.predict(X_test)


# ### Stacking model construction

# In[49]:


base_predictions_train = pd.DataFrame( {
    'DecisionTree': dt_train.ravel(),
        'RandomForest': rf_train.ravel(),
     'ExtraTrees': et_train.ravel(),
     'XgBoost': xg_train.ravel(),
    })
base_predictions_train.head(5)


# In[50]:


dt_train=dt_train.reshape(-1, 1)
et_train=et_train.reshape(-1, 1)
rf_train=rf_train.reshape(-1, 1)
xg_train=xg_train.reshape(-1, 1)
dt_test=dt_test.reshape(-1, 1)
et_test=et_test.reshape(-1, 1)
rf_test=rf_test.reshape(-1, 1)
xg_test=xg_test.reshape(-1, 1)


# In[51]:


x_train = np.concatenate(( dt_train, et_train, rf_train, xg_train), axis=1)
x_test = np.concatenate(( dt_test, et_test, rf_test, xg_test), axis=1)


# In[52]:


stk = xgb.XGBClassifier().fit(x_train, y_train)
y_predict=stk.predict(x_test)
y_true=y_test
stk_score=accuracy_score(y_true,y_predict)
print('Accuracy of Stacking: '+ str(stk_score))
precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted') 
print('Precision of Stacking: '+(str(precision)))
print('Recall of Stacking: '+(str(recall)))
print('F1-score of Stacking: '+(str(fscore)))
print(classification_report(y_true,y_predict))
cm=confusion_matrix(y_true,y_predict)
f,ax=plt.subplots(figsize=(5,5))
sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.savefig("heatmaps/TB_FS_StackModel.png")
# plt.show()


# In[ ]:




