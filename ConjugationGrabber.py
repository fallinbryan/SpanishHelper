

# Snags all the conjugations from the pickled verbList and creates a big data frame of verbs

import requests
from bs4 import BeautifulSoup as soup
import pickle
import pandas as pd
import numpy

verbTable = {'English': [], 'Spanish': [], 'Regular': [], 'Conjugations': []}
tableNames = ['Indicative',
              'Subjunctive',
              'Imperative',
              'Progressive',
              'Perfect',
              'Perfect Subjunctive']

with open('verbData.pickle','rb') as pickleFile:
    verbList = pickle.load(pickleFile)

for verb in verbList:
    print('Conjugating {}'.format(verb[1]))
    URL = 'http://www.spanishdict.com/conjugate/{}'.format(verb[1])
    conjugationClient = requests.get(URL)
    conjugationPage = conjugationClient.text
    conjugationClient.close()
    conjugationSoup = soup(conjugationPage, 'html.parser')
    pageDFList = pd.read_html(conjugationPage, flavor=['bs4'])
    conjugationDFs = []

    for i, name in enumerate(tableNames):
        df = pageDFList[i]
        df = df.rename(columns=df.iloc[0]).drop(df.index[0])
        df.rename(columns={numpy.nan: name}, inplace=True)
        conjugationDFs.append(df)

    verbTable['English'].append(verb[0])
    verbTable['Spanish'].append(verb[1])
    verbTable['Regular'].append(verb[2])
    verbTable['Conjugations'].append(conjugationDFs)

verb_df = pd.DataFrame(verbTable)
print('Pickling Verb Data')
with open('verbs.pickle','wb') as pickler:
    pickle.dump(verb_df,pickler)

print('Process Complete')
