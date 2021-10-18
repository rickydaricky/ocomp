hero_list = ['ana', 'ashe', 'baptiste', 'bastion', 'brigitte', 'dva', 'doomfist', 
'echo', 'genji', 'hanzo', 'junkrat', 'lucio', 'mccree', 'mei', 'mercy', 'moira', 
'orisa', 'pharah', 'reaper', 'reinhardt', 'roadhog', 'sigma', 'soldier76', 'sombra', 
'symmetra', 'torbjorn', 'tracer', 'widowmaker', 'winston', 'wreckingball', 'zarya', 'zenyatta']

def match(word, word_list):
    possibles = []
    for w in word_list:
        if w.startswith(word):
            possibles.add(w)
        if word is 