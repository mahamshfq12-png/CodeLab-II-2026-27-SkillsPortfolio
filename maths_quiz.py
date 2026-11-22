import math # import math module for calculations
import random # import random for generating question numbers
import tkinter as tk # import tkinter for window and widget creation
from tkinter import messagebox

BG_COLOUR = "#D9DCD9"
PANEL_COLOUR = "#F1F2F1" # define panel container and text theme colors
TEXT_COLOUR = "#1E2B22"
GREEN = "#1F4D2E"
GREEN_DARK = "#143320"
CORRECT_COLOUR = "#2E7D32"
WRONG_COLOUR = "#A0402D"
FONT = "Trebuchet MS"

TOTAL_QUESTIONS = 10 # set total questions per quiz session to 10
DIFFICULTIES = {"Easy": (1, 9), "Moderate": (10, 99), "Advanced": (1000, 9999)} # configure number range dictionaries for each difficulty level
GRADES = ((90, "A+"), (80, "A"), (70, "B"), (60, "C"), (50, "D"), (0, "F"))


def label(parent, text="", size=12, bold=False, fg=TEXT_COLOUR, bg=BG_COLOUR, **options): # helper function to quickly generate styled labels
    font = (FONT, size, "bold") if bold else (FONT, size)
    return tk.Label(parent, text=text, font=font, bg=bg, fg=fg, **options)


