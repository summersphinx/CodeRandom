from pycipher import Caesar


def shift(key, string):
    return Caesar(key).encipher(string).lower()


def flip(string):
    string = list(string)
    string.reverse()
    string = ''.join(string)
    return string


def encrypt(string, word):
    char = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
    string = list(string)

    new_word = ''

    for each in word:
        new_word += string[char.index(each)]
    return new_word
