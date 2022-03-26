import random as r
import PySimpleGUI as sg
import os
import string
import webbrowser
import time
import pygame
import urllib3
import base64
import socket

from mods import load_words
from mods import ciphers

# Custom theme


sg.LOOK_AND_FEEL_TABLE['CodeyGreen'] = {'BACKGROUND': '#000000',
                                        'TEXT': '#7FFF00',
                                        'INPUT': '#333',
                                        'TEXT_INPUT': '#7FFF00',
                                        'SCROLL': '#99CC99',
                                        'BUTTON': ('#7FFF00', '#000'),
                                        'PROGRESS': ('#D1826B', '#CC8019'),
                                        'BORDER': 1, 'SLIDER_DEPTH': 0,
                                        'PROGRESS_DEPTH': 0, }

sg.theme('GrayGrayGray')

global dir_path
# noinspection PyRedeclaration
dir_path = os.getcwd() + '/game'

global h_name
# noinspection PyRedeclaration
h_name = socket.gethostname()


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
    except Exception:
        f = open(path + '/' + file)
        x = f.read()
        return x


def save_settings(output):
    save_file = open(dir_path + "/settings.txt", "w")
    save_file.write(str(output))
    save_file.close()


def get_keys(dictionary):
    dict_list = []
    for key in dictionary.keys():
        dict_list.append(key)

    return dict_list


global SETTINGS
# noinspection PyRedeclaration
SETTINGS = read_file('settings.txt', dir_path)
run_game = True

# Levels

http = urllib3.PoolManager()

with open(dir_path + '/img/icon.png', 'rb') as png:
    png_str = base64.b64encode(png.read())


def open_mixer():
    # noinspection PyTypeChecker
    mixer_layout_left = [
        [sg.Text('Volume')],
        [sg.Slider((0, 1), default_value=SETTINGS['volume'], resolution=0.1, k='volume')]
    ]

    # mixer_layout_right = [[sg.Checkbox(text, 1), ] for text in os.listdir(dir_path + "/mp3/bg")]
    mixer_layout_right = [[]]

    mixer_layout = [
        [sg.Column(mixer_layout_left),
         sg.Column(mixer_layout_right)],
        [sg.Button('Ok')]
    ]

    w = sg.Window('Mixer', mixer_layout)

    while True:
        event2, values2 = w.read()
        if event2 in ('Ok', None):
            SETTINGS['volume'] = values2['volume']
            break
    w.close()


dev = False
if h_name == 'msi-gavin':
    if sg.PopupYesNo('Use Dev Levels?'):
        dev = True

# Game Settings
while run_game:

    if dev:
        levels = http.request('GET', 'https://github.com/summersphinx/CodeRandom-Stuff/raw/main/1/demo-levels.txt')
    else:
        levels = http.request('GET', 'https://github.com/summersphinx/CodeRandom-Stuff/raw/main/1/demo-levels.txt')
    levels = levels.data
    levels = eval(levels)

    sg.theme('GrayGrayGray')

    SETTINGS = read_file('settings.txt', dir_path)

    song = dir_path + "/mp3/bg/" + r.choice(os.listdir(dir_path + "/mp3/bg"))

    pygame.mixer.init()
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(999)
    # noinspection PyTypeChecker
    pygame.mixer.music.set_volume(SETTINGS['volume'])
    # noinspection PyTypeChecker
    if SETTINGS['mute']:
        pygame.mixer.music.set_volume(0.0)

    char = 'abcdefghijklmnopqrstuvwxyz'

    layout_left = [
        [sg.Text('Level')],
        [sg.Text('Theme')],
        [sg.Text('Time Trial')]
    ]
    Settings = True

    # Right side of the settings window
    # noinspection PyTypeChecker
    layout_right = [
        [sg.InputCombo(get_keys(levels), default_value=SETTINGS['difficulty'], k='difficulty', s=(21, 1))],
        [sg.InputCombo(
            ['CodeyGreen', 'Black', 'Dark', 'DarkBlue16', 'DarkGrey', 'DarkGreen5', 'DarkGrey12', 'LightBlue6',
             'Purple', 'Python', 'Reddit'], k='custom_theme', default_value=SETTINGS['custom_theme'])],
        [sg.Checkbox('', default=True, k='stopwatch_active')]
    ]

    # combine settings layouts
    # noinspection PyTypeChecker
    settings_layout = [
        [sg.Menu([['Music', ['Mute', 'Mixer']]])],
        [sg.Text('Settings', justification='center')],
        [sg.Column(layout_left, background_color=None),
         sg.Column(layout_right, background_color=None, element_justification='right')],
        [sg.Button('https://bit.ly/3pS66pe', k='help'), sg.Text(
            'is a valuable \nresource that is all about this game!\nOr the html page that comes with the game......')],
        [sg.Button('Play', k='start_game_from_settings')]
    ]

    window = sg.Window('CodeRandom', settings_layout, finalize=True, font='Comic 18 bold', size=(600, 400),
                       titlebar_icon=png_str)

    while Settings:

        event, values = window.read()

        print(event)

        if event in (None, 'Quit'):
            run_game = False
            break
        elif event == 'Mute':
            # noinspection PyTypeChecker
            if SETTINGS['mute']:
                # noinspection PyTypeChecker
                pygame.mixer.music.set_volume(float(SETTINGS['volume']))

            else:
                pygame.mixer.music.set_volume(0.0)
            # noinspection PyTypeChecker
            SETTINGS['mute'] = not SETTINGS['mute']

        elif event == 'Mixer':
            open_mixer()
        elif event == 'start_game_from_settings':
            break

        if values['stopwatch_active']:
            start_time = int(time.time())
            timing = True
        else:
            timing = False

    window.close()

    if not run_game:
        break

    # noinspection PyUnboundLocalVariable
    sg.theme(values['custom_theme'])
    # noinspection PyTypeChecker
    values['volume'] = SETTINGS['volume']
    # noinspection PyTypeChecker
    values['mute'] = SETTINGS['mute']
    save_settings(values)

    # Load Master Puzzle and Hint Puzzles

    puzzle_steps = levels.get(values['difficulty'])

    if 'tap' not in puzzle_steps:
        master_puzzle = r.choice(load_words.load_words(r.randint(4, 7)))
    else:
        master_puzzle = r.choice(load_words.load_words(r.randint(3, 5)))

    iteration = 0
    for each in puzzle_steps:
        if each == 'shift':
            key_shift = r.randint(1, 25)
            # noinspection PyTypeChecker
            puzzle_steps[iteration] = ([each, key_shift])
        elif each == 'flip':
            key_shift = r.randint(0, 25)
            # noinspection PyTypeChecker
            puzzle_steps[iteration] = ([each, key_shift])
        elif each == 'autokey':
            key_shift = r.choice(load_words.load_words(4)).upper()
            # noinspection PyTypeChecker
            puzzle_steps[iteration] = ([each, key_shift])
        iteration += 1

    print(puzzle_steps)

    master_puzzle_encrypted = [sg.Text('Master Puzzle: ')]

    for letter in master_puzzle:
        if 'pig' in puzzle_steps:
            master_puzzle_encrypted.append(
                sg.Image(source='{}/img/{}/pig_{}.png'.format(dir_path, values['custom_theme'],
                                                              ciphers.encrypt(puzzle_steps, letter)[0])))
    if 'pig' not in puzzle_steps:
        master_puzzle_encrypted.append(sg.Text(ciphers.encrypt(puzzle_steps, master_puzzle)))

    hint_order = []

    print(puzzle_steps)

    step_num = 0

    for step in puzzle_steps:
        hint_letters = r.sample(string.ascii_lowercase, k=3)
        original_letters = hint_letters.copy()

        if type(step) is list:

            if step[0] == 'shift':
                letters = ciphers.string_from_list(hint_letters)
                letters = ciphers.shift(step[1], letters)
                hint_order.append([original_letters, list(letters)])

            if step[0] == 'flip':
                letters = ciphers.string_from_list(hint_letters)
                # noinspection PyRedeclaration
                letters = ciphers.encipher(ciphers.flip(string.ascii_lowercase, step[1]), hint_letters)
                hint_order.append([original_letters, list(letters)])

            if step[0] == 'autokey':
                letters = ciphers.string_from_list(hint_letters)
                # noinspection PyRedeclaration
                letters = ciphers.autokey(step[1], hint_letters)

                hint_order.append([original_letters, list(letters)])

        if step == 'none':
            hint_order.append('none')
        step_num += 1

    current_hint = 0
    # hint_order[current_hint][0][0] + ' -> ' + hint_order[current_hint][1][0] + '\n' + hint_order[current_hint][0][1] + ' -> ' + hint_order[current_hint][1][1] + '\n' + hint_order[current_hint][0][2] + ' -> ' + hint_order[current_hint][1][2]
    # Notes

    from pycipher import Caesar as C

    table_b = []
    upper_char = list(string.ascii_uppercase)
    iteration = 0

    for i in string.ascii_uppercase:
        table_b.append([upper_char[iteration]] + list(C(iteration).encipher(string.ascii_lowercase).lower()))
        iteration += 1

    notes_layout = [[sg.Frame('', [
        [sg.Table(table_b, num_rows=27, vertical_scroll_only=False, hide_vertical_scroll=True, auto_size_columns=False,
                  col_widths=[2] * 27, headings=[' '] + list(string.ascii_uppercase))]],
                              size=(580, 710))]]

    # Hints Puzzles

    hint_card_layout = []

    print(len(hint_order))

    for each in hint_order:
        if puzzle_steps[current_hint][0] == 'autokey':
            hint_card_layout.append(
                sg.Frame('', layout=[[sg.Text(str(current_hint + 1) + '. Key:\n' + puzzle_steps[current_hint][1] + '\n',
                                              background_color='#787878',
                                              text_color=r.choice(
                                                  ['#ff0000', '#00ff00', '#0000ff', '#000000']))]],
                         element_justification='center',
                         size=(100, 150), background_color='#787878'))
            current_hint += 1
        else:
            hint_card_layout.append(sg.Frame('', layout=[[sg.Text(str(current_hint + 1) + '.\n' +
                                                                  hint_order[current_hint][0][0] + ' -> ' +
                                                                  hint_order[current_hint][1][0] + '\n' +
                                                                  hint_order[current_hint][0][1] + ' -> ' +
                                                                  hint_order[current_hint][1][1] + '\n' +
                                                                  hint_order[current_hint][0][2] + ' -> ' +
                                                                  hint_order[current_hint][1][2],
                                                                  background_color='#787878',
                                                                  text_color=r.choice(
                                                                      ['#ff0000', '#00ff00', '#0000ff', '#000000']))]],
                                             element_justification='center',
                                             size=(100, 150), background_color='#787878'))
            current_hint += 1

    hint_p_layout = [
        hint_card_layout
    ]

    # Master Puzzle
    # noinspection PyTypeChecker
    hint_m_layout = [
        master_puzzle_encrypted,
        [sg.Input('', k='input_master', s=(15, 1)), sg.Button('Test', k='test_master')]
    ]

    # Main Window

    puzzle_layout = [[sg.Frame('', hint_m_layout, size=(610, 350))],
                     [sg.Frame('', [[sg.Column(hint_p_layout, scrollable=True, size=(610, 340))]], size=(610, 350))]]

    toolbar = [sg.Text('CodeRandom'), sg.Button('Help'), sg.Button('Quit')]

    layout = [
        toolbar,
        [sg.Frame('', [[sg.Column(puzzle_layout, size=(620, 720))]]),
         sg.Frame('', [[sg.Column(notes_layout, size=(640, 720))]])]
    ]

    bug_layout = [
        [sg.Text('Email Form')],
        [sg.DropDown(['Bug', 'Issue', 'Suggestion'], default_value='Bug', k='type'), sg.Text('Email: '),
         sg.Input('', k='user_email')],
        [sg.Multiline('', k='msg', s=(75, 20))],
        [sg.Button('Submit', k='go')]
    ]

    # time.sleep(7)

    wn = sg.Window('CodeRandom', layout, finalize=True, font='Verdana 16 bold', size=(1280, 800))

    while True:

        event, values = wn.read()

        if event in ('Quit', None):
            sg.PopupOK('The word is: ' + master_puzzle)
            wn.close()
            break
        if event == 'Help':
            webbrowser.open_new_tab("https://coderandom.w3spaces.com/")
            continue

        if event in 'test_master':
            if values['input_master'].lower() == master_puzzle:
                # noinspection PyUnboundLocalVariable
                if timing:
                    end_time = int(time.time())
                    # noinspection PyUnboundLocalVariable
                    msg = 'You are Correct! Took {} Seconds'.format(end_time - start_time)
                else:
                    msg = 'You are Correct!'
                pygame.mixer.music.load(dir_path + "/mp3/effects/win.mp3")
                pygame.mixer.music.stop()
                pygame.mixer.music.play()
                sg.PopupOK(msg)
            if values['input_master'] != master_puzzle:
                sg.PopupOK('You are Incorrect!')
                continue
        if event == 'update_hint_p':
            pass
        if event == 'test_hint':
            if values['user_hint'] == master_puzzle:
                if timing:
                    end_time = int(time.time())
                    msg = 'You are Correct! Took {} Seconds'.format(end_time - start_time)
                else:
                    msg = 'You are Correct!'
                pygame.mixer.music.load(dir_path + "/mp3/win.mp3")
                pygame.mixer.music.stop()
                pygame.mixer.music.play()
                sg.PopupOK(msg)
            if values['user_hint'] != master_puzzle:
                sg.PopupOK('You are Incorrect!')
                continue
        wn.close()

pygame.mixer.music.stop()
