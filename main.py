from cgi import test
import os
from matplotlib import transforms
import pandas as pd
from sklearn.pipeline import Pipeline
import pipelines_fun
import matplotlib.pyplot as plt 
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

#load the data form the dataset folder
#len(name) >= 8 to avoid "cmds" file
ham_files    = [name for name in sorted(os.listdir("datasets\spam\easy_ham")) if len(name) >= 8]
spam_files   = [name for name in sorted(os.listdir("datasets\spam\spam")) if len(name) >= 8]

ham_files.append(0)
spam_files.append(1)

full_pipeline = Pipeline([
    ('read raw', pipelines_fun.Open_mails()),
    ('subject var',pipelines_fun.get_variables_from_object()),
    ('text var',pipelines_fun.GetVariableFromText()),
])

#create two dataframe
print("--------------spam")
df_spam         = full_pipeline.fit_transform(spam_files)
print("--------------ham")
df_ham          = full_pipeline.fit_transform(ham_files)

df_total = pd.concat([df_spam,df_ham],axis=0,join="outer",ignore_index=True)

#shuffle and split the dataset into training and test sets
split = StratifiedShuffleSplit(n_splits = 1, test_size = 0.2, random_state = 42)

for train_index, test_index in split.split(df_total, df_total["label"]):
	train_set = df_total.loc[train_index]
	test_set = df_total.loc[test_index]

def compare_var(var):
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(10,5))

    ax1.hist(train_set.loc[train_set["label"]==0][var],bins=50)
    ax2.hist(train_set.loc[train_set["label"]==1][var],bins=50)

    fig.suptitle(f"{var} distribution")
    ax1.set_title("ham")
    ax2.set_title("spam")

    plt.show()

compare_var("(T) is HTML")
print(train_set.head())

train_set_y = train_set["label"]
train_set   = train_set.drop(["label"],axis = 1)

test_set_y  = test_set["label"]
test_set    = test_set.drop(["label"],axis = 1)

print(type(train_set.loc[51]))
#model
forest_clf = RandomForestClassifier(random_state=42)
forest_clf.fit(train_set,train_set_y)
forest_clf.predict(train_set.loc[51].array.reshape(1,len(train_set.loc[51])))

print("------",train_set_y[51])