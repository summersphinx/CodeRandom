import os

dirPath = os.getcwd()


def load_words(size):
    with open(dirPath + '\\mods\\words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

        valid_words_2 = []

        for each in valid_words:
            if len(each) == size:
                valid_words_2.append(each)

    return valid_words_2
