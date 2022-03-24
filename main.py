import os
from sklearn.pipeline import Pipeline
import pipelines_fun


#load the data form the dataset folder
#len(name) >= 8 to avoid "cmds" file
ham_files    = [name for name in sorted(os.listdir("datasets\spam\easy_ham")) if len(name) >= 8]
spam_files   = [name for name in sorted(os.listdir("datasets\spam\spam")) if len(name) >= 8]

spam = True

full_pipeline = Pipeline([
    ('read raw', pipelines_fun.open_mails()),
])

df = full_pipeline.fit_transform(spam_files)

print(df.iloc[1])