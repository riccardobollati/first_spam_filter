import os
import pandas as pd
from sklearn.pipeline import Pipeline
import pipelines_fun
import matplotlib.pyplot as plt 
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit

#load the data form the dataset folder
#len(name) >= 8 to avoid "cmds" file
ham_files    = [name for name in sorted(os.listdir("datasets\spam\easy_ham")) if len(name) >= 8]
spam_files   = [name for name in sorted(os.listdir("datasets\spam\spam")) if len(name) >= 8]

ham_files.append(0)
spam_files.append(1)

full_pipeline = Pipeline([
    ('read raw', pipelines_fun.Open_mails()),
    ('subject var',pipelines_fun.get_variables_from_object()),
])

#create two dataframe
df_spam         = full_pipeline.fit_transform(spam_files)
spam_subject_df = df_spam.drop(["raw"],axis=1)

df_ham          = full_pipeline.fit_transform(ham_files)
spam_subject_df = df_ham.drop(["raw"],axis=1)

df_total = pd.concat([df_spam,df_ham],axis=0,join="outer",ignore_index=True)

#shuffle and split the dataset
split = StratifiedShuffleSplit(n_splits = 1, test_size = 0.2, random_state = 42)

for train_index, test_index in split.split(df_total, df_total["label"]):
	strat_train_set = df_total.loc[train_index]
	strat_test_set = df_total.loc[test_index]

print(strat_test_set["label"].value_counts())
print(strat_train_set["label"].value_counts())

#data for violin
# clr_ham  = df_ham["caps lock ratio"].tolist()#.append([np.NaN]*(len(df_spam)-len(df_ham)))
# clr_spam = df_spam["caps lock ratio"].tolist()

clr_df = pd.DataFrame([df_spam["caps lock ratio"],df_ham["caps lock ratio"]])

fig, (ax1, ax2) = plt.subplots(1,2)

ax1.hist(df_ham["caps lock ratio"],bins=50)
ax2.hist(df_spam["caps lock ratio"],bins=50)

fig.suptitle("caps lock ratio distribution")
ax1.set_title("ham")
ax2.set_title("spam")

plt.show()