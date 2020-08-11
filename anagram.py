from letterFreq import *

def sameNumLetters(fileFreq, dictFreq):
    if len(fileFreq) != len(dictFreq):
        return False
    for key in fileFreq:
        if fileFreq.get(key) != dictFreq.get(key):
            return False
    return True
# part 1
def anagram_sets(file):
    anagrams = []
    currentAnagram = []
    dictFreqs = open('words_alpha.txt', mode='r')
    for fileWord in file:
        currentAnagram.append(fileWord.strip())
        for word in dictFreqs:
            fileFreq = freq_letters(fileWord.strip())
            wordFreq = freq_letters(word.strip())
            if fileWord.strip() != word.strip() and sameNumLetters(fileFreq, wordFreq):
                currentAnagram.append(word.strip())
        anagrams.append(currentAnagram)
        currentAnagram = []
        dictFreqs.seek(0)
    return anagrams

# part 2
def sortAnagrams():
    file = open('words.txt', mode='r')
    anagrams = anagram_sets(file)
    return sorted(anagrams)   

print(sortAnagrams())
