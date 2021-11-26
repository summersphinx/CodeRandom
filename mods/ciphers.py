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
    return string


def string_from_list(l):
    word = ''

    for char in l:
        word += char
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
                print(word)

        else:
            if step == 'flip':
                word = flip(word)

        word = list(word)

    return word


print(encrypt([['shift', 3], 'flip'], 'baby'))
