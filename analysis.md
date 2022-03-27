# pipeline results
the output of the pipe line is a dataframe containing the following variables:
- label: the desired output
- include ?: 1 if the subject include the question mark simble
- include $: 1 if the subject include the dollar symbol
- include free: 1 if the subject include the word "free"
- include save: 1 if the subject include the word "save"
- include best: 1 if the subject include the word "best"
- caps lock ratio: is the upper character to lower character ratio
- number of !: the number of exclamation point that the subject include
- empty : 1 if the subject is empty

all those variables has been extracted from the raw text through the pipeline, they have been selected after a quick look at some mails to get insights
