import os
import pandas as pd
from sklearn.pipeline import Pipeline
import pipelines_fun
import matplotlib.pyplot as plt 
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import cross_val_predict

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
print("--------------processing spam mails")
df_spam         = full_pipeline.fit_transform(spam_files)
print("--------------processing ham mails")
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

def plot_precision_recall_vs_threshold(precisions, recalls, thresholds):
    plt.plot(thresholds, precisions[:-1], "b--", label="Precision", linewidth=2)
    plt.plot(thresholds, recalls[:-1], "g-", label="Recall", linewidth=2)
    plt.legend(loc="center right", fontsize=16)
    plt.xlabel("Threshold", fontsize=16)        

print(train_set.head())

train_set_y = train_set["label"]
train_set   = train_set.drop(["label"],axis = 1)

test_set_y  = test_set["label"]
test_set    = test_set.drop(["label"],axis = 1)

#model
log_reg = LogisticRegression(solver="lbfgs", max_iter=1000, random_state=42)
log_reg.fit(train_set,train_set_y)
y_predict = log_reg.decision_function(train_set)

# precision = precision_score(test_set_y,y_predict)
# recall = recall_score(test_set_y,y_predict)
# print("prec: ",precision," recall: ",recall)

precision, recall, threshold = precision_recall_curve(train_set_y,y_predict)

plot_precision_recall_vs_threshold(precision, recall, threshold)
plt.figure()

plt.plot(recall,precision)
plt.show()
