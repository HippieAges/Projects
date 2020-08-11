# chapter 14 exercises

# exercise 1
def sed(patternstr, replstr, file1, file2):
    if patternstr in file1.read():
        file1.seek(0)
        readFile = file1.read()
        file2.write(readFile.replace(patternstr, replstr))
    else:
        file1.seek(0)
        file2.write(file1.read())

with open("file1.txt", 'r') as file1, open("file2.txt", 'w') as file2:
    sed("Hello", "Goodbye", file1, file2)