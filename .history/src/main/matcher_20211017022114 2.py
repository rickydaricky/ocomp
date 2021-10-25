hero_list = ['ana', 'ashe', 'baptiste', 'bastion', 'brigitte', 'dva', 'doomfist', 
'echo', 'genji', 'hanzo', 'junkrat', 'lucio', 'mccree', 'mei', 'mercy', 'moira', 
'orisa', 'pharah', 'reaper', 'reinhardt', 'roadhog', 'sigma', 'soldier76', 'sombra', 
'symmetra', 'torbjorn', 'tracer', 'widowmaker', 'winston', 'wreckingball', 'zarya', 'zenyatta']

def match(word, word_list):
    possibles = []
    for w in word_list:
        if w.startswith(word):
            possibles.add(w)
    length_possibles = len(possibles)
    if length_possibles != 1:
        raise ValueError('no hero could be found with that name, and it does not appear to be an abbreviation either')
    return possibles[0]