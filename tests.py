all_words = ''
long_line = ''
questions = set({'who', 'what', 'where', 'when', 'why', 'how'})
while(True):
    words = input("Say something: ").lower()
    all_words = words.split()
    if all_words[0] in questions:
        all_words[-1] += '? '
        long_line += ' '.join(all_words).capitalize()
    elif words != '\end':
        all_words[-1] += '. '
        long_line += ' '.join(all_words).capitalize()

    if words == '\end':
        break

print(long_line)