import random as r, math, os, time, urllib, webbrowser, PySimpleGUI as sg
from mods import load_words

# Custom theme

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

dirPath = os.getcwd() + '\\game'

# Create a var for game settings

def readFile(file, path):

     try:
         f = open(path + '\\' + file)
         x = f.read()
         newDict = eval(x) #turn into tuple
         dict(newDict)
         f.close()
         return newDict
     except:
         f = open(path + '\\' + file)
         x = f.read()
         return

def save_settings(output):
    save_file = open(dirPath + "\\game\\settings.txt", "w")
    save_file.write(str(output))
    save_file.close()

global SETTINGS
SETTINGS = readFile('settings.txt', dirPath)

# Game Settings

def make_settings_wn(dirPath):

    # settings layout

    layout_left = [
        [sg.Text('Difficulty')],
        [sg.Text('Notes Window')],
        [sg.Text('Theme')]
        ]

    layout_right = [
        [sg.Spin([i for i in range(1,11)], initial_value=SETTINGS['difficulty'], k='difficulty', s=(2, 1))],
        [sg.Checkbox('', default=SETTINGS['have_notes'], k='toggle_notes')],
        [sg.InputCombo(sg.theme_list(), k='custom_theme', default_value=SETTINGS['last_theme'])]
        ]

    layout = [[sg.Text('Settings', justification = 'center', expand_x = True)],
        [sg.Column(layout_left, background_color = None, expand_y = True, expand_x = True),
        sg.Column(layout_right, background_color = None, expand_y = True, expand_x = True, element_justification = 'right')],
        [sg.Button('Play', k='start_game_from_settings'), sg.Button("", image_filename=dirPath + '\\img\\information_i.png', size=(30, 30), button_color=None, key="settings_help")]
        ]

    return sg.Window('CodeRandom', layout, finalize=True, font=('Comic 18 bold'), size=(600, 400))

# make a window to show the master puzzle

def make_master_puzzle(wordlength):

    master_word = r.choice(load_words.load_words(wordlength))

    master_layout = [[sg.Text(master_word)]]

    return sg.Window('CodeRandom - Master Puzzle', master_layout, location = (620, 10), finalize=True, font=('Comic 18'), size=(600, 400))

# Create a window for the user to store notes

def make_notes_wn():

    #find the notes file

    n = open(dirPath + '\\notes.txt', 'r')

    # store notes in multiline element

    notes_layout = [
        [sg.Text("Notes"), sg.Button("Save", k='notes_save'), sg.Button("", image_filename=dirPath + '\\img\\information.png', size=(30, 30), button_color=None, key="notes_help")],
        [sg.Multiline(n.read(), expand_x = True, expand_y = True, k='Notes')]
        ]

    n.close()

    return sg.Window('CodeRandom - Notes', notes_layout, location = (10, 10), finalize=True, font=('Comic 18'), size=(600, 400))

def make_main_win():

    # create the different parts in the main window

    main_menu_layout = [
        [sg.Text("CodeRandom")],
        [sg.Text('Answer:'), sg.Input(k='user_answer'), sg.Button('Test', k='test_user_answer')]
        ]

    toolbar = [
        [sg.Button("Quit", k='toolbar_quit'), sg.Button("", image_filename=dirPath + '\\img\\information.png', size=(30, 30), button_color=None, key="Help")]
        ]

    layout = [[toolbar], [
        sg.Column(main_menu_layout, k='main_menu_layout', expand_x = True, expand_y = True, background_color=(None)),
        
        ]]

    return sg.Window('CodeRandom', layout, size = (750, 500), finalize=True, font=('Comic 18'))

def main():

    # bools for if windows are open or not

    is_settings_wn = False
    is_notes_wn = False
    is_main_wn = False
    is_master_wn = False

    # open the settings window

    settings_wn = make_settings_wn(dirPath)
    is_settings_wn = True

    while True:

        # read the next event

        wn, event, values = sg.read_all_windows()

        if event in ('settings_help', 'notes_help', 'main_help'):

            webbrowser.open_new_tab(dirPath + "\\html\\Help.html")

        if event == 'start_game_from_settings':

            SETTINGS['difficulty'] = values['difficulty']
            
            if values['toggle_notes'] and not is_notes_wn: # open notes wn

                sg.theme(values['custom_theme'])
                notes_wn = make_notes_wn()
                is_notes_wn = True

        if event in ('quit', None):
            
            try:
                settings_wn.close()
            except:
                pass
            try:
                notes_wn.close()
            except:
                pass
            break
        

main()




















