import os
import string
from sklearn.base import BaseEstimator, TransformerMixin
import email
import email.policy
from email.parser import Parser
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

scaler = StandardScaler()

class Open_mails(BaseEstimator, TransformerMixin ):
    
    def __init__(self):
        pass

    def fit(self, X):
        return self
    
    def transform(self, raw):
        
        X = pd.DataFrame()
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
        
        #special char ratio:
        spec_char_ratio = []
        #word included bool:
        include_free = []
        include_save = []
        include_best = []
        #caps lock word ratio float:
        CL_ratio = []
        #number of exclamation points int:
        #is subject empty?
        text_p = []

        # print(mail.get("Subject"))
        # print(mail.get_payload())

        for i in X["raw"]:
            
            text = i.get("Subject")
            #number of scec char :
            ex = sum(1 for elem in text if elem == "!")
            qm = sum(1 for elem in text if elem == "?")
            dl = sum(1 for elem in text if elem == "$")
            if len(text) > 0:
                spec_char_ratio.append((ex + qm + dl)/len(text))
            else:
                spec_char_ratio.append(0)
            #word included bool:
            include_free.append(int("free" in text.lower()))
            include_save.append(int("save" in text.lower()))
            include_best.append(int("best" in text.lower()))
            #caps lock ratio
            if len(text) > 0 :
                CL_ratio.append(sum(1 for elem in text if elem.isupper())/len(text.replace(" ","")))
            else:
                CL_ratio.append(0)
            text_p.append(text)

        
        #X["special char"]     = scaler.fit_transform(np.array(number_of_spec_char).reshape(-1, 1))
        X["(S) special char ratio"] = spec_char_ratio
        X["(S) include free"]       = include_free
        X["(S) include save"]       = include_save
        X["(S) include best"]       = include_best
        X["(S) caps lock ratio"]    = CL_ratio
        X["(S) subject_text"]       = text_p

        return X

class GetVariableFromText(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        pass
    def fit(self, X):
        return self
    
    def transform(self,X):

        urls_number       = []
        special_chr_ratio = []
        upper_case_ratio  = []
        
        for i in X["raw"]:

            text = i.get_payload()

            if isinstance(text,list):
                text = str(text[0]).split(" ")
            else:
                text = str(text).split(" ")
            urln = 0

            #get the number of urls
            for index, word in enumerate(text):
                
                if "http://" in word:
                    
                    urln = urln + 1
                    del text[index]

            urls_number.append(urln)

            text = "".join(text)
            
            if len(text):
                special_ratio_num = sum(1 for letter in text if letter not in list(string.ascii_letters))/len(text)
                upper_case_num    = sum(1 for letter in text if letter.isupper())/len(text)

            special_ratio_num   = 0
            upper_case_num      = 0

            special_chr_ratio.append(special_ratio_num)
            upper_case_ratio.append(upper_case_num)

        X["(T) urls number"]         = urls_number
        X["(T) special char ratio"]  = special_chr_ratio
        X["(T) upper case ratio"]    = upper_case_ratio

        X = X.drop(["raw"],axis=1)

        return X
