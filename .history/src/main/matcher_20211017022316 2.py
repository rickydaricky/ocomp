def word_match(word, word_list):
    possibles = []
    for w in word_list:
        if w.startswith(word):
            possibles.append(w)
    length_possibles = len(possibles)
    if length_possibles != 1:
        raise ValueError('no hero could be found with that name, and it does not appear to be an abbreviation either')
    return possibles[0]