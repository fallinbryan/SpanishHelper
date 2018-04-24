
# Scrapes the top 100 verbs from www.linguasorb.com/spanish/verbs/most-common
# packs the verbs into a pickle

import requests
from bs4 import BeautifulSoup as soup
import pickle
verbListClient = None
verbListURLS = [ 'https://www.linguasorb.com/spanish/verbs/most-common-verbs/',
                 'https://www.linguasorb.com/spanish/verbs/most-common-verbs/2',
                 'https://www.linguasorb.com/spanish/verbs/most-common-verbs/3',
                 'https://www.linguasorb.com/spanish/verbs/most-common-verbs/4']
verbList = []
for url in verbListURLS:
    print('Scraping {}'.format(url))
    verbListClient = requests.get(url)
    page = verbListClient.text
    pageSoup = soup(page,'html.parser')
    verbTable = pageSoup.findAll('table', {'id': 'verbTable'})
    verbRows = verbTable[0].findAll('tr')
    for row in verbRows:
        isRegular = True
        try:
            if len(row.findAll('td')[1].a.findAll('span', {'class': 'vIrreg'})) > 0:
                isRegular = False
            else:
                isRegular = True

            if isRegular:
                verbList.append((row.findAll('td')[2].text, row.findAll('td')[1].a.span.text, 'regular'))
            else:
                verbList.append((row.findAll('td')[2].text, row.findAll('td')[1].a.span.text, 'irregular'))
        except:
            pass

verbListClient.close()
with open('verbData.pickle', 'wb') as pickleFile:
    pickle.dump(verbList, pickleFile)

print('Verb Data Pickled')
