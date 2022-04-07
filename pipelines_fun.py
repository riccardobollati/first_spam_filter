import os
import string
from sklearn.base import BaseEstimator, TransformerMixin
import email
import email.policy
from email.parser import Parser
import pandas as pd
import warnings

import re
from html import unescape

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

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

        
        #X["special char"]     = scaler.fit_transform(np.array(number_of_spec_char).reshape(-1, 1))
        X["(S) special char ratio"] = spec_char_ratio
        X["(S) include free"]       = include_free
        X["(S) include save"]       = include_save
        X["(S) include best"]       = include_best
        X["(S) caps lock ratio"]    = CL_ratio

        return X

def html_to_plain_text(html):
    text = re.sub('<head.*?>.*?</head>', '', html, flags=re.M | re.S | re.I)
    text = re.sub('<a\s.*?>', ' HYPERLINK ', text, flags=re.M | re.S | re.I)
    text = re.sub('<.*?>', '', text, flags=re.M | re.S)
    text = re.sub(r'(\s*\n)+', '\n', text, flags=re.M | re.S)
    return unescape(text)
            
def email_to_text(email):
    html = None
    for part in email.walk():
        ctype = part.get_content_type()
        if not ctype in ("text/plain", "text/html"):
            continue
        try:
            content = part.get_content()
        except: # in case of encoding issues
            content = str(part.get_payload())
        if ctype == "text/plain":
            return content
        else:
            html = content
    if html:
        return html_to_plain_text(html)

class GetVariableFromText(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        pass
    def fit(self, X):
        return self
    
    def transform(self,X):

        urls_number       = []
        special_chr_ratio = []
        upper_case_ratio  = []
        mail_type         = []
        is_empty          = []
        
        for i in X["raw"]:

            text = i.get_payload()

            if isinstance(text,list):
                
                mail_type.append("multipart({})".format(", ".join([sub_email.get_content_type() for sub_email in text])))
                text = str(text[0])
            
            else:
                mail_type.append(i.get_content_type())
            
            #extract plain text from HTML
            text = email_to_text(i)
            if len(text):
                text = text.split(" ")

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
            else:
                special_ratio_num   = 0
                upper_case_num      = 0


            special_chr_ratio.append(special_ratio_num)
            upper_case_ratio.append(upper_case_num)

        X["(T) urls number"]         = urls_number
        X["(T) special char ratio"]  = special_chr_ratio
        X["(T) upper case ratio"]    = upper_case_ratio
        X["(T) text type"]           = mail_type

        X = X.drop(["raw"],axis=1)

        return X
