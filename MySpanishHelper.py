import pandas as pd
import pickle
import tkinter as tk
import numpy as np
import random

def isInt(str):
    try:
        i = int(str)
        return True
    except:
        return False

moodMap = {'Indicative': 0,
           'Subjunctive': 1,
           'Imperative': 2,
           'Progressive': 3,
           'Perfect': 4,
           'Perfect Subjunctive': 5}

blockMoods = ['Perfect Subjunctive','Perfect']

pronounMap = {'yo': 0,
              'tú': 1,
              'Ud.': 2,
              'nosotros': 3,
              'vosotros': 4,
              'Uds': 5}



tenses = ['Present',
          'Preterite',
          'Imperfect',
          'Conditional',
          'Future',
          'Imperfect 2',
          'Affirmative',
          'Negative',
          'Past']
block_tenses = ['Conditional',
                'Future',
                'Imperfect 2',
                'Past']

block_forms = ['Preterite Subjunctive',
               'Imperfect Subjunctive',
               'Affirmative Progressive',
               'Negative Progressive',
               'Negative Indicative',
               'Affirmative Indicative',
               'Affirmative Subjunctive',
               'Present Imperative',
               'Imperfect Imperative',
               'Negative Subjunctive',
               'Imperfect Progressive',
               'Preterite Imperative',
               'Preterite Progressive']

headers = ['English', 'Spanish', 'Regular', 'Conjugations']

moods = []
pronouns = []
for name in moodMap:
    moods.append(name)
for name in pronounMap:
    pronouns.append(name)


with open('verbs.pickle','rb') as pickledData:
    verbs_df = pickle.load(pickledData)

verb_list = verbs_df.Spanish.values

verbMap = {}
for i,verb in enumerate(verb_list):
    verbMap[verb] = i

all_words = [v for v in verb_list]
verb_blocks = []
start_index = len(all_words)
end_index = len(all_words)
for lst in verbs_df['Conjugations'].values:
    verb_blocks.append( (start_index, end_index) )
    start_index = end_index
    for index, df in enumerate(lst):
        for name in df.drop(columns=moods[index]):
            for word in df[name].values:
                all_words.append(word)
                end_index += 1
verb_blocks.append( (start_index, end_index) )
verb_blocks.pop(0)

response_key = 0
tries = 0.0
number_correct = 0.0
print('\n\n')
print('**<<------------------>>WELCOME TO MySpanishHelper<<------------------------->>**')

while response_key >= 0:
    tries += 1
    random_verb = verb_list[random.randrange(0, len(verb_list))]
    rMood = moods[random.randrange(0, len(moods))]
    while rMood in blockMoods:
        rMood = moods[random.randrange(0, len(moods))]
    rTense = tenses[random.randrange(0, len(tenses))]
    while rTense in block_tenses:
        rTense = tenses[random.randrange(0, len(tenses))]

    while '{} {}'.format(rTense, rMood) in block_forms:
        rMood = moods[random.randrange(0, len(moods))]
        while rMood in blockMoods:
            rMood = moods[random.randrange(0, len(moods))]
        rTense = tenses[random.randrange(0, len(tenses))]
        while rTense in block_tenses:
            rTense = tenses[random.randrange(0, len(tenses))]

    rForm = pronouns[random.randrange(0, len(pronouns))]
    question_String = 'What is the {} {} {} form of the verb {} ?'.format(
        rTense, rMood, rForm, random_verb
    )
    answerDFList = verbs_df['Conjugations'].values[verbMap[random_verb]]
    answerMoodDF = answerDFList[moodMap[rMood]]
    try:
        answerTenseCol = answerMoodDF[rTense].values
        answer = answerTenseCol[pronounMap[rForm]]
    except KeyError:
        answer = 'No such Tense for Mood'
    verb_block = verb_blocks[verbMap[random_verb]]
    answer_List = [answer]
    st = verb_block[0]
    en = verb_block[1]
    for i in range(7):
        random_word = all_words[random.randrange(st, en)]
        while random_word == answer:
            random_word = all_words[random.randrange(st, en)]
        answer_List.append(random_word)
    random.shuffle(answer_List)
    answer_index = answer_List.index(answer)
    print('\n\n')
    print(question_String)
    print('Choose a number from the following list, or enter -1 to exit')
    for i, word in enumerate(answer_List):
        print('{}\t{}'.format(i+1,word))

    response = input(': ANSWER HERE >')
    while not isInt(response):
        print('Invalid Response')
        response = input(': ANSWER HERE >')

    response_key = int(response)-1


    if response_key == 98:

        english = verbs_df.English.values[verbMap[random_verb]]
        regularity = verbs_df.Regular.values[verbMap[random_verb]]
        print('{} is {} verb.'.format(random_verb,regularity))
        print('English translations: {}'.format(english))

        response = input(': ANSWER HERE >')
        while not isInt(response):
            print('Invalid Response')
            response = input(': ANSWER HERE >')
        response_key = int(response) - 1

    if response_key == answer_index:

        print("Correct!")
        number_correct += 1
    else:
        print('else',response_key, answer_index)
        if response_key >= 0:

            print("Sorry that is Incorrect..")
            print('The correct answer is {}'.format(answer))


tries -= 1
print('\n\n\n')
print('Thank you for playing')
print('Your Score was {0:.1f}%'.format((number_correct/tries)*100))
