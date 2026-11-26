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


BLOB_STYLES = [(2.7, 0.045, 3, 0.9), (2.5, 0.05, 2, 0.3), (2.9, 0.04, 3, 3.5)]


class CloudButton(tk.Canvas): # start custom canvas CloudButton class definition
    HOVER_LIFT = 4
    PRESS_SINK = 2
    created = 0

    def __init__(self, parent, text, command, width, height, fill, hoverFill, textColour, shadowColour, font):
        self.base = parent.cget("bg")
        super().__init__(parent, width=width, height=height, bg=self.base, highlightthickness=0, bd=0, cursor="hand2")
        self.command, self.buttonState, self.pressed, self.faceOffset = command, "normal", False, 0
        fade = lambda colour, amount: self.mix(colour, self.base, amount) 
        self.colours = {   # map out color states for hover and click effects
            "normal": (fill, textColour, shadowColour),
            "hover": (hoverFill, textColour, fade(shadowColour, 0.35)),
            "disabled": (fade(fill, 0.6), fade(textColour, 0.4), fade(shadowColour, 0.7)),
        }
        x, y = width / 2, height - 9 
        self.shadowRings = [
            self.create_oval(x - width * 0.42 * k, y - 6 * k, x + width * 0.42 * k, y + 6 * k, outline="") # create ovals to render a layered drop shadow
            for k in (1 - i * 0.12 for i in range(7))
        ]
        roundness, wobble, lobes, turn = BLOB_STYLES[CloudButton.created % 3]
        CloudButton.created += 1
        raw = [] # compute math points to give buttons cloud shape
        for i in range(32):
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
        self.create_polygon(points, smooth=True, splinesteps=30, outline="", tags=("cloud", "face")) # draw cloud polygon shape on canvas
        self.create_text(width / 2, 4 + blobHeight / 2, text=text, font=font, tags=("label", "face"))
        self.refresh("normal")
        self.bind("<Enter>", self.onEnter)
        self.bind("<Leave>", self.onLeave)
        self.bind("<ButtonPress-1>", self.onPress)
        self.bind("<ButtonRelease-1>", self.onRelease)

    def mix(self, colour1, colour2, amount):
        rgb = lambda colour: [v // 256 for v in self.winfo_rgb(colour)]
        return "#%02x%02x%02x" % tuple(round(a + (b - a) * amount) for a, b in zip(rgb(colour1), rgb(colour2)))

    def refresh(self, mode):
        fill, textColour, shadow = self.colours["disabled" if self.buttonState == "disabled" else mode]
        self.itemconfigure("cloud", fill=fill)
        self.itemconfigure("label", fill=textColour)
        for i, ring in enumerate(self.shadowRings):
            self.itemconfigure(ring, fill=self.mix(self.base, shadow, 0.9 * (i + 1) / 7))

    def shift(self, target):
        self.move("face", 0, target - self.faceOffset)
        self.faceOffset = target

    def onEnter(self, event): # handle mouse enter event
        if self.buttonState == "normal":
            self.refresh("hover")
            self.shift(-self.HOVER_LIFT)

    def onLeave(self, event): # handle mouse leave event
        self.refresh("normal")
        self.shift(0)

    def onPress(self, event): # handle mouse press event
        if self.buttonState == "normal":
            self.pressed = True
            self.shift(self.PRESS_SINK)

    def onRelease(self, event): # handle mouse release event
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
