from pycipher import Caesar
from string import ascii_lowercase


def shift(key, string):
    return Caesar(key).encipher(string).lower()


def flip(word):
    string = list(ascii_lowercase)
    string.reverse()
    new_word = ''
    for each in word:
        new_word += string[ascii_lowercase.index(each)]
    string = ''.join(string)
    return new_word


def string_from_list(l):
    word = ''

    for char in l:
        word += char
    return word


def tap(word):
    key = {
        'a': (1, 1),
        'b': (2, 1),
        'c': (3, 1),
        'd': (4, 1),
        'e': (5, 1),
        'f': (1, 2),
        'g': (2, 2),
        'h': (3, 2),
        'i': (4, 2),
        'j': (5, 2),
        'k': (3, 1),
        'l': (1, 3),
        'm': (2, 3),
        'n': (3, 3),
        'o': (4, 3),
        'p': (5, 3),
        'q': (1, 4),
        'r': (2, 4),
        's': (3, 4),
        't': (4, 4),
        'u': (5, 4),
        'v': (1, 5),
        'w': (2, 5),
        'x': (3, 5),
        'y': (4, 5),
        'z': (5, 5)
    }
    new_word = []
    for each in word:
        new_word.append(key[each])
    return new_word


def encipher(string, word):
    char = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
    string = list(string)

    new_word = ''

    for each in word:
        new_word += string[char.index(each)]
    return new_word


def encrypt(steps, word):
    for step in steps:
        if type(step) == list:
            if step[0] == 'shift':
                word = shift(step[1], word)
                print('d:')
                print(word)
        else:
            if step == 'flip':
                word = flip(word)
            elif step == 'tap':
                word = tap(word)

        word = list(word)

    return word
