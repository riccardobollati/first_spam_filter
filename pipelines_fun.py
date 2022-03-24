from cProfile import label
import os
from unicodedata import name
from sklearn.base import BaseEstimator, TransformerMixin
import email
import email.policy
from email.parser import Parser
import pandas as pd


class Open_mails(BaseEstimator, TransformerMixin ):
    
    def __init__(self):
        pass

    def fit(self, X):
        return self
    
    def transform(self, raw):
        
        X = pd.DataFrame()
        print(raw[-1])
        raw_list = []
        directory = "spam" if raw[-1] else "easy_ham"

        for name in raw[:-1]:
            
            with open(os.path.join("datasets\spam\\", directory, name), "rb") as f:
            
                raw_list.append(email.parser.BytesParser(policy=email.policy.default).parse(f))
        
        X["raw"] = raw_list
        X["label"] = raw[-1]

        return X

class get_variables_from_object(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self,X):
        return self
    
    def transform(self,X):
        
        #simbol included bool:
        include_q_mark = []
        include_dollar = []
        #word included bool:
        include_free = []
        include_save = []
        include_best = []
        #caps lock word ratio float:
        CL_ratio = []
        #number of exclamation points int:
        N_expoints =[]
        #is subject empty?
        empty = []
        text_p = []

        # print(mail.get("Subject"))
        # print(mail.get_payload())

        for i in X["raw"]:
            
            text = i.get("Subject")
            #check if include:
            include_q_mark.append("?" in text)
            include_dollar.append("$" in text)
            #word included bool:
            include_free.append("free" in text.lower())
            include_save.append("save" in text.lower())
            include_best.append("best" in text.lower())
            #number of exclamation points
            N_expoints.append(sum(1 for elem in text if elem == "!"))
            #caps lock ratio
            if len(text) > 0 :
                CL_ratio.append(sum(1 for elem in text if elem.isupper())/len(text.replace(" ","")))
                empty.append(False)
            else:
                CL_ratio.append(0)
                empty.append(True)
            text_p.append(text)

        
        X["include ?"]        = include_q_mark
        X["include $"]        = include_dollar
        X["include free"]     = include_free
        X["include save"]     = include_save
        X["include best"]     = include_best
        X["caps lock ratio"]  = CL_ratio
        X["number of !"]      = N_expoints
        X["empty"]            = empty
        X["subject_text"]     = text_p



        return X






