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


BLOB_STYLES = [(2.7, 0.045, 3, 0.9), (2.5, 0.05, 2, 0.3), (2.9, 0.04, 3, 3.5)] # define shape variations for the custom cloud buttons


class CloudButton(tk.Canvas):
    HOVER_LIFT = 4
    PRESS_SINK = 2
    created = 0
    # start of the custom canvas CloudButton class
    def __init__(self, parent, text, command, width, height, fill, hoverFill, textColour, shadowColour, font):
        self.base = parent.cget("bg")
        super().__init__(parent, width=width, height=height, bg=self.base, highlightthickness=0, bd=0, cursor="hand2")
        self.command, self.buttonState, self.pressed, self.faceOffset = command, "normal", False, 0
        fade = lambda colour, amount: self.mix(colour, self.base, amount)
        self.colours = {                  # setup colour dictionary for hover, normal and disabled states
            "normal": (fill, textColour, shadowColour),
            "hover": (hoverFill, textColour, fade(shadowColour, 0.35)),
            "disabled": (fade(fill, 0.6), fade(textColour, 0.4), fade(shadowColour, 0.7)),
        }
        x, y = width / 2, height - 9
        self.shadowRings = [                   # generate soft shadow rings underneath the button
            self.create_oval(x - width * 0.42 * k, y - 6 * k, x + width * 0.42 * k, y + 6 * k, outline="")
            for k in (1 - i * 0.12 for i in range(7))
        ]
        roundness, wobble, lobes, turn = BLOB_STYLES[CloudButton.created % 3]
        CloudButton.created += 1
        raw = []
        for i in range(32):    # use sin wave math to calculate organic blob curves
            angle = 2 * math.pi * i / 32
            radius = 1 + wobble * math.sin(lobes * angle + turn)
            raw.append([math.copysign(abs(f(angle)) ** (2 / roundness), f(angle)) * radius for f in (math.cos, math.sin)])
        xs, ys = zip(*raw)
        blobHeight = height - 24
        points = [
            value for px, py in raw for value in (
                3 + (px - min(xs)) / (max(xs) - min(xs)) * (width - 6),
                4 + (py - min(ys)) / (max(ys) - min(ys)) * blobHeight)
        ]
        self.create_polygon(points, smooth=True, splinesteps=30, outline="", tags=("cloud", "face")) # draw the final polygon shape onto the cnvas
        self.create_text(width / 2, 4 + blobHeight / 2, text=text, font=font, tags=("label", "face"))
        self.refresh("normal")
        self.bind("<Enter>", self.onEnter)
        self.bind("<Leave>", self.onLeave)
        self.bind("<ButtonPress-1>", self.onPress)
        self.bind("<ButtonRelease-1>", self.onRelease)

    def mix(self, colour1, colour2, amount):
        rgb = lambda colour: [v // 256 for v in self.winfo_rgb(colour)]
        return "#%02x%02x%02x" % tuple(round(a + (b - a) * amount) for a, b in zip(rgb(colour1), rgb(colour2)))

    def refresh(self, mode): # refresh button color dynamically based on mouse interaction
        fill, textColour, shadow = self.colours["disabled" if self.buttonState == "disabled" else mode]
        self.itemconfigure("cloud", fill=fill)
        self.itemconfigure("label", fill=textColour)
        for i, ring in enumerate(self.shadowRings): 
            self.itemconfigure(ring, fill=self.mix(self.base, shadow, 0.9 * (i + 1) / 7))

    def shift(self, target): # animate button face moving up or down on click
        self.move("face", 0, target - self.faceOffset)
        self.faceOffset = target

    def onEnter(self, event):
        if self.buttonState == "normal":
            self.refresh("hover")
            self.shift(-self.HOVER_LIFT)

    def onLeave(self, event):
        self.refresh("normal")
        self.shift(0)

    def onPress(self, event):
        if self.buttonState == "normal":
            self.pressed = True
            self.shift(self.PRESS_SINK)

    def onRelease(self, event):
        if not self.pressed:
            return
        self.pressed = False
        inside = 0 <= event.x <= int(self.cget("width")) and 0 <= event.y <= int(self.cget("height"))
        self.refresh("hover" if inside else "normal")
        self.shift(-self.HOVER_LIFT if inside else 0)
        if inside:
            self.command()

    def configure(self, cnf=None, **kwargs):
        if "text" in kwargs:
            self.itemconfigure("label", text=kwargs.pop("text"))
        if "state" in kwargs:
            self.buttonState = kwargs.pop("state")
            self.shift(0)
            self.refresh("normal")
            super().configure(cursor="hand2" if self.buttonState == "normal" else "arrow")
        if cnf or kwargs:
            return super().configure(cnf, **kwargs)

    config = configure