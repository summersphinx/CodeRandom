import random as r
import PySimpleGUI as sg
import os
import string
import webbrowser
import time
import pygame

from mods import load_words
from mods import ciphers

# Levels

levels = {
    'Introduction': ['shift'],
    'Flipping Things Up': ['flip'],
    '2 is True': ['shift', 'flip'],
    'Oink Oink': ['pig'],
    '3 Peas in a Pod': ['shift', 'flip', 'tap'],
    'Tapping the System': ['tap'],
    'A Small Inconvenience': ['shift', 'flip', 'pig']
}

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

    song = dir_path + "/mp3/bg/" + r.choice(os.listdir(dir_path + "/mp3/bg"))
    print(song)

    pygame.mixer.init()
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(999)

    char = 'abcdefghijklmnopqrstuvwxyz'


    def make_settings_wn():
        # Left side of the settings window

        layout_left = [
            [sg.Text('Level')],
            [sg.Text('Theme')],
            [sg.Text('Lives')],
            [sg.Text('Time Trial')]
        ]

        # Right side of the settings window
        layout_right = [
            [sg.Spin(get_keys(levels), initial_value=SETTINGS['difficulty'], k='difficulty', s=(21, 1))],
            [sg.InputCombo(
                ['CodeyGreen', 'Black', 'Dark', 'DarkBlue16', 'DarkGrey', 'DarkGreen5', 'DarkGrey12', 'LightBlue6',
                 'Purple', 'Python', 'Reddit'], k='custom_theme', default_value=SETTINGS['custom_theme'])],
            [sg.Checkbox('', default=False, k='do_lives', disabled=True)],
            [sg.Checkbox('', default=True, k='stopwatch_active')]
        ]

        # combine settings layouts
        settings_layout = [[sg.Text('Settings', justification='center')],
                           [sg.Column(layout_left, background_color=None),
                            sg.Column(layout_right, background_color=None, element_justification='right')],
                           [sg.Button('Play', k='start_game_from_settings'), sg.Button('Custom Game', k='custom')]
                           ]

        return sg.Window('CodeRandom', settings_layout, finalize=True, font='Comic 18 bold', size=(600, 400))


    def make_custom_wn():

        # Custom Game Layout
        settings_layout = [
            [sg.Text('Custom Game', justification='center')],
            [sg.Text('Game Settings')],
            [sg.InputCombo(
                ['CodeyGreen', 'Black', 'Dark', 'DarkBlue16', 'DarkGrey', 'DarkGreen5', 'DarkGrey12', 'LightBlue6',
                 'Purple', 'Python', 'Reddit'], k='custom_theme', default_value=SETTINGS['last_theme'])],
            [sg.Spin([1, 2, 3, 4], k='steps'), sg.Text('Step Count')],
            [sg.Checkbox('Stopwatch', default=True, k='stopwatch_active')],
            [sg.Text('Game Ciphers')],
            [sg.Checkbox('Shift', k='shift')],
            [sg.Checkbox('Flip', k='flip')],
            [sg.Checkbox('Pigpen', k='pig')],
            [sg.Button('Play', k='start_game_from_custom')]
        ]

        return sg.Window('CodeRandom - Custom', settings_layout, finalize=True, font='Comic 18 bold', size=(400, 600),
                         no_titlebar=True)


    window = make_settings_wn()

    event, values = window.read()

    if event != 'start_game_from_settings' and event != 'custom':
        break

    if event == 'custom':
        window.close()
        custom = make_custom_wn()
        event2, values2 = custom.read()
        if event2 != 'start_game_from_custom':
            break
        custom.close()

    if values['stopwatch_active']:
        start_time = int(time.time())
        timing = True
    else:
        timing = False

    window.close()

    if event == 'custom':

        # noinspection PyUnboundLocalVariable
        sg.theme(values2['custom_theme'])
        save_settings(values2)
    else:
        sg.theme(values['custom_theme'])
        save_settings(values)

    # Load Master Puzzle and Hint Puzzles

    if event != 'custom':
        puzzle_steps = levels.get(values['difficulty'])

    else:
        new_steps = [None]
        if values2['shift']:
            new_steps.append('shift')
        if values2['flip']:
            new_steps.append('flip')
        if values2['pig']:
            new_steps.append('pig')
        print(new_steps)
        puzzle_steps = []
        for i in range(values2['steps']):
            puzzle_steps.append(r.choice(new_steps))

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

    notes_layout = [[sg.Frame('', [[sg.Text("Notes")],
                                   [sg.Multiline(n.read(), size=(30, 24))]], size=(640, 600))]

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
                                                                  hint_order[current_hint][1][2])]],
                                             element_justification='center', size=(120, 150)))
            current_hint += 1

    hint_p_layout = [
        hint_card_layout
    ]

    # Master Puzzle
    # noinspection PyTypeChecker
    hint_m_layout = [
        master_puzzle_encrypted,
        [sg.Image(dir_path + '/img/heart.png', background_color=None),
         sg.Image(dir_path + '/img/heart.png', background_color=None),
         sg.Image(dir_path + '/img/heart.png', background_color=None)],
        [sg.Input('', k='input_master', s=(15, 1)), sg.Button('Test', k='test_master')]
    ]

    # Main Window

    puzzle_layout = [[sg.Frame('', hint_m_layout, size=(620, 350))],
                     [sg.Frame('', hint_p_layout, size=(620, 350))]]

    toolbar = [sg.Text('CodeRandom'), sg.Button('Help'), sg.Button('Report Bugs'), sg.Button('Quit')]

    layout = [
        toolbar,
        [sg.Frame('', [[sg.Column(puzzle_layout, size=(620, 700))]]),
         sg.Frame('', [[sg.Column(notes_layout, size=(640, 700))]])]
    ]

    # time.sleep(7)

    wn = sg.Window('CodeRandom', layout, finalize=True, no_titlebar=True, font='Verdana 16 bold', size=(1280, 720))

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
        if event == 'Form':
            webbrowser.open_new_tab('https://forms.gle/sMgiRuVWcKewB8wa7')
        if event == 'Report Bugs':
            webbrowser.open_new_tab('https://github.com/summersphinx/CodeRandom/issues')
        if event in 'test_master':
            if values['input_master'].lower() == master_puzzle:
                if timing:
                    end_time = int(time.time())
                    print(end_time)
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
                    print(end_time)
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
