import math # import math for button coordinate calculations
import os
import random
import tkinter as tk # import tkinter for building the GUI window
from tkinter import messagebox

NAVY = "#14213D"
NAVY_LIGHT = "#1F3A66"
POWDER_BLUE = "#B0E0E6" # setup navy blue colour theme variables
POWDER_DARK = "#8CC8D2"
WHITE_BLUE = "#E8F6F9"
FONT = "Verdana"
JOKE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "randomJokes.txt") # define file path to load random jokes from text file


def loadJokes(filename): # function to load and parse jokes line by line
    jokes = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            if "?" in line:
                setup, punchline = line.strip().split("?", 1)
                jokes.append((setup.strip() + "?", punchline.strip())) # strip whitespace and save tuples into the joke list
    return jokes