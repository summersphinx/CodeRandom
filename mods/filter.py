import os

dirPath = os.getcwd()

def filter_words(minimum, maximum):
    with open(dirPath + '\\words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

        words = []

        for each in valid_words:
            l = len(each)
            if l >= minimum or l <= maximum:
                words.append(each)
        for each in words:

            valid_words.remove(each)
        print(valid_words)
        return (valid_words)


words = filter_words(7, 4)

print(type(words))

new_file = ''

for each in words:
    new_file += each + '\n'
print(new_file)
