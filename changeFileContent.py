import string

# exercise 1
readingFile = open('2274.txt', mode='r')

splitLine = []
strippedWords = [] 
for i in readingFile:
    splitLine = i.strip().split(" ")
    puncTable = str.maketrans(dict.fromkeys(string.punctuation))
    whiteSpaceTable = str.maketrans(dict.fromkeys(string.whitespace))
    for j in splitLine:
        if j not in string.whitespace:
            strippedWords.append(j.translate(puncTable).translate(whiteSpaceTable).lower())
# print(strippedWords)

# exercise 2
bookWords = {}
for word in strippedWords:
    bookWords[word] = bookWords.setdefault(word, 0) + 1

print(bookWords)
print(sum(bookWords.values()))