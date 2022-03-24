import os
from sklearn.pipeline import Pipeline
import pipelines_fun


#load the data form the dataset folder
#len(name) >= 8 to avoid "cmds" file
ham_files    = [name for name in sorted(os.listdir("datasets\spam\easy_ham")) if len(name) >= 8]
spam_files   = [name for name in sorted(os.listdir("datasets\spam\spam")) if len(name) >= 8]

ham_files.append(0)
spam_files.append(1)

print(spam_files[-1])

full_pipeline = Pipeline([
    ('read raw', pipelines_fun.Open_mails()),
    ('subject var',pipelines_fun.get_variables_from_object()),
])

df = full_pipeline.fit_transform(spam_files)

print(df.iloc[20])