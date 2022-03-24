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

class read_mails(BaseEstimator, TransformerMixin):
    def fit(self,X):
        return self
    
    def transform(self,X):
        return self





