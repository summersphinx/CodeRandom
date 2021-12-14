import random as r
import PySimpleGUI as sg
import os
import string
import webbrowser
import time
import pygame

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

# Game Settings
while True:
    sg.theme('GrayGrayGray')

    SETTINGS = read_file('settings.txt', dir_path)

    song = dir_path + "/mp3/bg/" + r.choice(os.listdir(dir_path + "/mp3/bg"))
    print(song)

    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.init()
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(song), loops=999)
    pygame.mixer.Channel(0).set_volume(0.4)
    # pygame.mixer.Channel(1).play(pygame.mixer.Sound(dir_path + '/tutorial/talk/hello.mp3'))

    char = 'abcdefghijklmnopqrstuvwxyz'

    def new_instructions(new):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound(dir_path + '/tutorial/talk/' + new))


    def make_settings_wn():
        # Left side of the settings window

        layout_left = [
            [sg.Text('Theme')],
        ]

        # Right side of the settings window
        # noinspection PyTypeChecker
        layout_right = [
            [sg.InputCombo(
                ['CodeyGreen', 'Black', 'Dark', 'DarkBlue16', 'DarkGrey', 'DarkGreen5', 'DarkGrey12', 'LightBlue6',
                 'Purple', 'Python', 'Reddit'], k='custom_theme', default_value=SETTINGS['custom_theme'])]
        ]

        # combine settings layouts
        settings_layout = [[sg.Text('Settings', justification='center')],
                           [sg.Column(layout_left, background_color=None),
                            sg.Column(layout_right, background_color=None, element_justification='right')],
                           [sg.Text('CodeRandom.w3spaces.com is a valuable \nresource that is all about this game!')],
                           [sg.Button('Play', k='start_game_from_settings')]
                           ]

        return sg.Window('CodeRandom', settings_layout, finalize=True, font='Comic 18 bold', size=(600, 400))


    window = make_settings_wn()

    event, values = window.read()

    if event != 'start_game_from_settings' and event != 'custom':
        break

    timing = False

    window.close()

    sg.theme(values['custom_theme'])

    # Load Master Puzzle and Hint Puzzles

    puzzle_steps = ['shift', 'flip', 'pig']

    if 'tap' not in puzzle_steps:
        master_puzzle = r.choice(load_words.load_words(r.randint(4, 7)))
    else:
        master_puzzle = r.choice(load_words.load_words(r.randint(3, 5)))

    iteration = 0
    for each in puzzle_steps:
        print('a:')
        print(each)
        if each == 'shift':
            key_shift = r.randint(1, 25)
            # noinspection PyTypeChecker
            puzzle_steps[iteration] = ([each, key_shift])
            print("b:")
            print(puzzle_steps)
        iteration += 1

    print('c:')
    print(master_puzzle)
    master_puzzle_encrypted = [sg.Text('Master Puzzle: ')]

    for letter in master_puzzle:
        if 'pig' in puzzle_steps:
            master_puzzle_encrypted.append(
                sg.Image(source=dir_path + '/img/' + values['custom_theme'] + '/pig_' + ciphers.encrypt(puzzle_steps, letter)[0] + '.png'))
        elif 'tap' in puzzle_steps:
            master_puzzle_encrypted.append(sg.Text(ciphers.encrypt(puzzle_steps, letter)[0]))
        else:
            master_puzzle_encrypted.append(sg.Text(ciphers.encrypt(puzzle_steps, letter)[0]))

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

        if step == 'flip':
            letters = ciphers.string_from_list(hint_letters)
            # noinspection PyRedeclaration
            letters = ciphers.encipher(ciphers.flip(string.ascii_lowercase), hint_letters)
            hint_order.append([original_letters, list(letters)])

        if step == 'none':
            hint_order.append('none')
        step_num += 1

    current_hint = 0
    # hint_order[current_hint][0][0] + ' -> ' + hint_order[current_hint][1][0] + '\n' + hint_order[current_hint][0][1] + ' -> ' + hint_order[current_hint][1][1] + '\n' + hint_order[current_hint][0][2] + ' -> ' + hint_order[current_hint][1][2]
    # Notes

    n = open(dir_path + '\\notes.txt', 'r')  # Read Stored Notes

    notes_layout = [[sg.Frame('', [[sg.Multiline(n.read(), size=(37, 27))]], size=(580, 690))]

                    ]

    n.close()

    # Hints Puzzles

    hint_card_layout = []

    for each in hint_order:
        if each == 'none':
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
                                             text_color=r.choice(['#ff0000', '#00ff00', '#0000ff', '#000000']))]],
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
                     [sg.Frame('', hint_p_layout, size=(610, 350))]]

    toolbar = [sg.Text('CodeRandom'), sg.Button('Quit')]

    layout = [
        toolbar,
        [sg.Frame('', [[sg.Column(puzzle_layout, size=(620, 720))]]),
         sg.Frame('Notes', [[sg.Column(notes_layout, size=(640, 710))]])]
    ]

    # time.sleep(7)

    wn = sg.Window('CodeRandom', layout, finalize=True, font='Verdana 16 bold', size=(1280, 800))

    print(sg.theme())

    while True:

        event, values = wn.read()

        if event in ('Quit', None):
            sg.PopupOK('The word is: ' + master_puzzle)
            print(values)
            wn.close()
            break
        if event == 'Help':
            webbrowser.open_new_tab("https://coderandom.w3spaces.com/")
            continue
        if event == 'Report Bugs':
            webbrowser.open_new_tab('https://github.com/summersphinx/CodeRandom/issues')
            continue
        if event in 'test_master':
            if values['input_master'].lower() == master_puzzle:
                if timing:
                    end_time = int(time.time())
                    print(end_time)
                    # noinspection PyUnboundLocalVariable
                    msg = 'You are Correct! Took {} Seconds'
                else:
                    msg = 'You are Correct!'
                pygame.mixer.Channel(0).play(pygame.mixer.Sound(dir_path + "/mp3/effects/win.mp3"))
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
                    print(end_time)
                    msg = 'You are Correct! Took {} Seconds'
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
