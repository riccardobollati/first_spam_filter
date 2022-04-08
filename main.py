import os
import pandas as pd
from sklearn.pipeline import Pipeline
import pipelines_fun
import matplotlib.pyplot as plt 
import numpy as np

from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import precision_score, recall_score

def compare_var(df, var):
        fig, (ax1, ax2) = plt.subplots(1,2,figsize=(10,5))

        ax1.hist(df.loc[df["label"]==0][var],bins=50)
        ax2.hist(df.loc[df["label"]==1][var],bins=50)

        fig.suptitle(f"{var} distribution")
        ax1.set_title("ham")
        ax2.set_title("spam")

        plt.show()

def plot_precision_recall_vs_threshold(precisions, recalls, thresholds):
    plt.plot(thresholds, precisions[:-1], "b--", label="Precision", linewidth=2)
    plt.plot(thresholds, recalls[:-1], "g-", label="Recall", linewidth=2)
    plt.legend(loc="center right", fontsize=16)
    plt.xlabel("Threshold", fontsize=16)


def main():
    #load the data form the dataset folder
    #len(name) >= 8 to avoid "cmds" file
    ham_files    = [name for name in sorted(os.listdir("datasets\spam\easy_ham")) if len(name) >= 8]
    spam_files   = [name for name in sorted(os.listdir("datasets\spam\spam")) if len(name) >= 8]

    ham_files.append(0)
    spam_files.append(1)

    full_pipeline = Pipeline([
        ('read raw', pipelines_fun.Open_mails()),
        ('subject var',pipelines_fun.get_variables_from_object()),
        ('text var', pipelines_fun.GetVariableFromText()),
        ('hot encoder', pipelines_fun.TypeHotEncoder()),
    ])

    #create two dataframe one for spam mails and one for ham mails
    print("--------------processing spam mails")
    df_spam         = full_pipeline.fit_transform(spam_files)
    print("--------------processing ham mails")
    df_ham          = full_pipeline.fit_transform(ham_files)

    #merge the two dataframe and return only one, filling Na
    df_total = pd.concat([df_spam,df_ham],axis=0,join="outer",ignore_index=True)
    df_total.fillna(0, inplace=True)

    print(df_total.head())

    #shuffle and split the dataset into training and test sets
    split = StratifiedShuffleSplit(n_splits = 1, test_size = 0.2, random_state = 42)

    for train_index, test_index in split.split(df_total, df_total["label"]):
        train_set = df_total.loc[train_index]
        test_set = df_total.loc[test_index]

    #divide X from labels
    train_set_y = train_set["label"]
    train_set   = train_set.drop(["label"],axis = 1)

    test_set_y  = test_set["label"]
    test_set    = test_set.drop(["label"],axis = 1)

    #model
    log_reg = LogisticRegression(solver= "lbfgs",random_state=42)
    
    #train the model
    log_reg.fit(train_set,train_set_y)

    #test the model
    y_predict_decision = log_reg.decision_function(test_set)
    y_predict = log_reg.predict(test_set)

    precision, recall, threshold = precision_recall_curve(test_set_y,y_predict_decision)
    
    #set the threshold to obtain a 90% precision
    th_90_precision = threshold[np.argmax(precision >= 0.9)]
    predict_n1_72_th = [i > th_90_precision for i in y_predict_decision]

    precision_th = precision_score(test_set_y,predict_n1_72_th)
    recall_th = recall_score(test_set_y,predict_n1_72_th)

    print("precision: ",precision_th," recall: ",recall_th)

    plot_precision_recall_vs_threshold(precision, recall, threshold)
    plt.axvline(x = th_90_precision,color = "r", ls = ":",alpha = 0.8)
    plt.plot([th_90_precision],[precision_th],"ro")
    plt.plot([th_90_precision],[recall_th],"ro")
    plt.figure()

    plt.plot(recall,precision)
    plt.plot([recall_th, recall_th], [0, precision_th],'r:')
    plt.plot([0, recall_th], [precision_th, precision_th],'r:')
    plt.plot([recall_th],[precision_th],"ro")
    plt.show()

if __name__ == "__main__":
    main()