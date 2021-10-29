import random as r, math, os, time, urllib, webbrowser, PySimpleGUI as sg
from mods import load_words

dirPath = os.getcwd() + '\\game'

pp = []

master_word = r.choice(load_words.load_words(5))

for each in master_word:
    s = dirPath+"\\img\\pig_"+each+".png"
    pp.append(sg.Image(s))

layout = [pp]
    
window = sg.Window('Test', layout)

event, values = window.read()

window.close()
print(master_word)
