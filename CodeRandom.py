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

dirPath = os.getcwd() + '/game'

# Create a var for game settings

def readFile(file, path):

     try:
         f = open(path + '/' + file)
         x = f.read()
         newDict = eval(x) #turn into tuple
         dict(newDict)
         f.close()
         return newDict
     except:
         f = open(path + '/' + file)
         x = f.read()
         return

def save_settings(output):
    save_file = open(dirPath + "/game/settings.txt", "w")
    save_file.write(str(output))
    save_file.close()

global SETTINGS
SETTINGS = readFile('settings.txt', dirPath)

# Game Settings

# Notes

# Hints Puzzles

# Master Puzzle

# Main Window

layout=[
     [sg.Menu([['&CodeRandom', ['&New', '&Settings', '&Help', '&Minimize', '&Quit']]], font='Verdana', pad=(10,10))]
        ]

wn = sg.Window('CodeRandom',layout, finalize = True, no_titlebar = True)
wn.maximize()

event, values = wn.read()

if event == 'Quit':
     print('print')

wn.close()







































