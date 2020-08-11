from operator import itemgetter

def freq_letters(word):
    letterFreq = {}
    for letter in word:
        letterFreq[letter] = letterFreq.get(letter, 0) + 1
    return letterFreq

def most_frequent(word):
    letterFreq = freq_letters(word)
    return sorted(list(letterFreq.items()), key=itemgetter(1), reverse=True)

# def new_most_frequent(word):
#     letterFreq = freq_letters(word)
#     return sorted(letterFreq, key=itemgetter(1), reverse=True)
# print(most_frequent("Pneumonoultramicroscopicsilicovolcanoconiosis"))
# print(new_most_frequent("Pneumonoultramicroscopicsilicovolcanoconiosis"))