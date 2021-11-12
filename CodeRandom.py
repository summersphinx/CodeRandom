import random as r
import os
import string
# import time
import webbrowser
import PySimpleGUI as sg
from pandas import read_csv

from mods import load_words
from mods import ciphers

# Custom theme

char = 'abcdefghijklmnopqrstuvwxyz'

sg.LOOK_AND_FEEL_TABLE['.CodeyGreen'] = {'BACKGROUND': '#000000',
                                         'TEXT': '#7FFF00',
                                         'INPUT': '#000',
                                         'TEXT_INPUT': '#7FFF00',
                                         'SCROLL': '#99CC99',
                                         'BUTTON': ('#7FFF00', '#000'),
                                         'PROGRESS': ('#D1826B', '#CC8019'),
                                         'BORDER': 1, 'SLIDER_DEPTH': 0,
                                         'PROGRESS_DEPTH': 0, }

sg.theme('GrayGrayGray')

global dir_path
dir_path = os.getcwd() + '/game'


# Create a var for game settings


def read_file(file, path):
    # read a file stored in the game
    # noinspection PyBroadException
    try:
        f = open(path + '/' + file)
        x = f.read()
        new_dict = eval(x)  # turn into tuple
        dict(new_dict)
        f.close()
        return new_dict
    except:
        f = open(path + '/' + file)
        x = f.read()
        return x


def save_settings(output):
    save_file = open(dir_path + "/game/settings.txt", "w")
    save_file.write(str(output))
    save_file.close()


global SETTINGS
SETTINGS = read_file('settings.txt', dir_path)


def get_levels():
    wb = read_csv(
        'https://docs.google.com/spreadsheets/d/12u8YjG8_XJnMxyZq6gjYZss5Ez2UU_KaMZe64cT5-7U/export?format=csv&gid=1923121378')
    return wb['Level'].values.tolist()


def get_level_plan(level):
    wb = read_csv(
        'https://docs.google.com/spreadsheets/d/12u8YjG8_XJnMxyZq6gjYZss5Ez2UU_KaMZe64cT5-7U/export?format=csv&gid=1923121378',
        index_col='Level')
    return wb.loc[level].values.tolist()


# Game Settings

def make_settings_wn(path):
    # Left side of the settings window

    layout_left = [
        [sg.Text('Difficulty')],
        [sg.Text('Theme')]
    ]

    # Right side of the settings window
    # noinspection PyTypeChecker
    layout_right = [
        [sg.Spin(get_levels(), k='difficulty', s=(20, 1))],
        [sg.InputCombo(sg.theme_list(), k='custom_theme', default_value=SETTINGS['last_theme'])]
    ]

    # combine settings layouts
    # noinspection PyTypeChecker
    settings_layout = [[sg.Text('Settings', justification='center', expand_x=True)],
                       [sg.Column(layout_left, background_color=None, expand_y=True, expand_x=True),
                        sg.Column(layout_right, background_color=None, expand_y=True, expand_x=True,
                                  element_justification='right')],
                       [sg.Button('Play', k='start_game_from_settings'),
                        sg.Button("", image_filename=path + '\\img\\information_i.png', size=(30, 30),
                                  button_color=None,
                                  key="settings_help")]
                       ]

    return sg.Window('CodeRandom', settings_layout, finalize=True, font='Comic 18 bold', size=(600, 400))


window = make_settings_wn(dir_path)

event, values = window.read()

if event == 'start_game_from_settings':
    launch_main_wn = True
else:
    launch_main_wn = False

window.close()

sg.theme(values['custom_theme'])

# Load Master Puzzle and Hint Puzzles

puzzle_steps = get_level_plan(values['difficulty'])

master_puzzle = r.choice(load_words.load_words(r.randint(4, 7)))

iteration = 0
for each in puzzle_steps:
    if each == 'shift':
        iteration += 1
        key_shift = r.randint(1, 25)
        char = ciphers.shift(key_shift, char)
        puzzle_steps.insert(iteration, [each, key_shift])
        puzzle_steps.pop(iteration - 1)
    elif each == 'flip':
        char = ciphers.flip(char)
    elif each == 'none':
        iteration += 1
        continue

print(char)
print(master_puzzle)

master_puzzle_encrypted = ciphers.encrypt(char, master_puzzle)

hint_puzzle_words = [r.choice(load_words.load_words(4)), r.choice(load_words.load_words(4)),
                     r.choice(load_words.load_words(4))]

hint_order = []


print(puzzle_steps)
for step in puzzle_steps:
    hint_letters = [r.choice(
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z']), r.choice(
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z']), r.choice(
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z'])]
    original_letters = hint_letters.copy()
    if type(step) is list:
        print(True)
        if step[0] == 'shift':
            letters = ciphers.string_from_list(hint_letters)
            letters = ciphers.shift(step[1], letters)
            hint_order.append([original_letters, list(letters)])
    if step == 'flip':
        print('flip')
        letters = ciphers.string_from_list(hint_letters)
        letters = ciphers.encrypt(ciphers.flip(string.ascii_lowercase), hint_letters)
        hint_order.append([original_letters, list(letters)])

current_hint = 0

hint_p_p = [sg.Text(hint_order[current_hint][0][0] + ' -> ' + hint_order[current_hint][1][0] + '\n' + hint_order[current_hint][0][1] + ' -> ' + hint_order[current_hint][1][1] + '\n' + hint_order[current_hint][0][2] + ' -> ' + hint_order[current_hint][1][2], k='hint_card')]
# hint_order[current_hint][0][0] + ' -> ' + hint_order[current_hint][1][0] + '\n' + hint_order[current_hint][0][1] + ' -> ' + hint_order[current_hint][1][1] + '\n' + hint_order[current_hint][0][2] + ' -> ' + hint_order[current_hint][1][2]
# Notes

n = open(dir_path + '\\notes.txt', 'r')  # Read Stored Notes

notes_layout = [
    [sg.Text("Notes")],
    [sg.Multiline(n.read(), expand_y=True, expand_x=True)]
]

n.close()

# Hints Puzzles


hint_p_layout = [
    [sg.Radio('A', 'hint_p', default=True, k=0),
     sg.Radio('B', 'hint_p', k=1),
     sg.Radio('C', 'hint_p', k=2), sg.Button('Update', k='update_hint_p')],
    [sg.Input('', k='user_hint'), sg.Button('Test', k='test_hint')],
    hint_p_p
]

# Master Puzzle
# noinspection PyTypeChecker
hint_m_layout = [
    [sg.Text('Master Puzzle: ' + master_puzzle_encrypted)],
    [sg.Text(puzzle_steps)],
    [sg.Image(dir_path + '/img/heart.png', background_color=None),
     sg.Image(dir_path + '/img/heart.png', background_color=None),
     sg.Image(dir_path + '/img/heart.png', background_color=None)],
    [sg.Input('', k='input_master'), sg.Button('Test', k='test_master')]
]

# Main Window

puzzle_layout = [[sg.Frame('', hint_m_layout, expand_x=True, expand_y=True)],
                 [sg.Frame('', hint_p_layout, expand_x=True, expand_y=True)]]

layout = [
    [sg.Menu([['&CodeRandom', ['&Form', '&Help', '&Report Bugs', '&Quit']]], font='Verdana', size=(24, 24), pad=(10, 10))],
    [sg.Column(notes_layout, expand_x=True, expand_y=True), sg.Column(puzzle_layout, expand_x=True, expand_y=True)]
]


if launch_main_wn:
    wn = sg.Window('CodeRandom', layout, finalize=True, no_titlebar=True, font='Verdana 16 bold')
    wn.maximize()

    while True:

        event, values = wn.read()

        if event in ('Quit', None):
            print(values)
            break
        if event == 'Help':
            webbrowser.open_new_tab(dir_path + "\\game\\html\\Help.html")
        if event == 'Form':
            webbrowser.open_new_tab('https://forms.gle/sMgiRuVWcKewB8wa7')
        if event == 'Report Bugs':
            webbrowser.open_new_tab('https://github.com/summersphinx/CodeRandom/issues/new')
        if event == 'update_hint_p':
            if values['0']:
                current_hint = 0
            if values['1']:
                current_hint = 1
            if values['2']:
                current_hint = 2
            # noinspection PyBroadException
            try:
                wn['hint_card'].update(hint_order[current_hint][0][0] + ' -> ' + hint_order[current_hint][1][0] + '\n' + hint_order[current_hint][0][1] + ' -> ' + hint_order[current_hint][1][1] + '\n' + hint_order[current_hint][0][2] + ' -> ' + hint_order[current_hint][1][2])
            except:
                wn['hint_card'].update('N/A')
        if event == 'test_master':
            if values['input_master'] == master_puzzle:
                sg.PopupOK('You are Correct!')
                break
            if values['input_master'] != master_puzzle:
                sg.PopupOK('You are Incorrect!')
        if event == 'update_hint_p':
            pass
        if event == 'test_hint':
            if values['user_hint'] == master_puzzle:
                sg.PopupOK('You are Correct!')
            if values['user_hint'] != master_puzzle:
                sg.PopupOK('You are Incorrect!')
    wn.close()
