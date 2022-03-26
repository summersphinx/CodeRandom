from pycipher import Caesar
from pycipher import Autokey
from string import ascii_lowercase


def shift(key, string):
    if type(string) == list:
        word = Caesar(key).encipher(string[0]).lower()
    else:
        word = Caesar(key).encipher(string).lower()
    return word


def flip(word, key):
    stuff = Caesar(key).encipher(ascii_lowercase).lower()
    stuff = list(stuff)
    stuff.reverse()
    stuff = ''.join(stuff)
    string = ''
    stuff = list(stuff)

    for letter in word:
        string += ascii_lowercase[stuff.index(letter)]
    return string


def string_from_list(list_to_be):
    word = ''

    for char in list_to_be:
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


def base5(word):
    key = {
        'a': '00',
        'b': '01',
        'c': '02',
        'd': '03',
        'e': '04',
        'f': '05',
        'g': '10',
        'h': '11',
        'i': '12',
        'j': '13',
        'k': '14',
        'l': '15',
        'm': '20',
        'n': '21',
        'o': '22',
        'p': '23',
        'q': '24',
        'r': '25',
        's': '30',
        't': '31',
        'u': '32',
        'v': '33',
        'w': '34',
        'x': '35',
        'y': '40',
        'z': '41'
    }
    new_word = []
    for each in word:
        new_word.append(key[each])
    return new_word


def autokey(key, word):
    print(word)
    if type(word) == list:
        word = Autokey(key.upper()).encipher(word[0]).lower()
    else:
        word = Autokey(key.upper()).encipher(word).lower()

    print(word)

    return word


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
            elif step[0] == 'flip':
                word = flip(word, step[1])
            elif step[0] == 'autokey':
                word = autokey(step[1], word)
        else:
            if step == 'tap':
                word = tap(word)
            elif step == 'base':
                word = base5(word)

    return word
