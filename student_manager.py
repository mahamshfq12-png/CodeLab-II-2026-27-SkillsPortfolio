import math # import math module for numeric calculations
import os # import os to handle directory paths for student data
import tkinter as tk # import tkinter and ttk widgets for desktop GUI
from collections import Counter # import counter from collections to tally grades
from dataclasses import dataclass
from tkinter import messagebox, ttk # import messagebox for data warnings and error

PINK = "#FFE6EA" # define pink theme colour pallete constants
PINK_DARK = "#F9CFD8"
BLACK = "#1A1A1A"
CHARCOAL = "#3D3D3D" # define dark charcoal and black colour for text
TEXT_COLOUR = "#1A1A1A"
ROW_EVEN = "#FFF8F6"
ROW_ODD = "#FFEAEE"
FAIL_TEXT = "#B3261E"
FONT = "Candara"
MONO_FONT = "Courier New"

COURSEWORK_MAX = 20
COURSEWORK_TOTAL = 60
EXAM_MAX = 100
TOTAL_MARKS = 160
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "studentMarks.txt")

TABLE_COLUMNS = [ # define table column headers, widhts and alignments
    ("name", "Name", 160, "w"),
    ("code", "ID", 80, "center"),
    ("coursework", "Coursework", 125, "center"),
    ("exam", "Exam", 100, "center"),
    ("percent", "Percent", 105, "center"),
    ("grade", "Grade", 85, "center"),
]

SORT_KEYS = {  # define lambda sorting keys or table columns
    "name": lambda s: s.name.lower(),
    "code": lambda s: s.code,
    "coursework": lambda s: s.courseworkTotal,
    "exam": lambda s: s.examMark,
    "percent": lambda s: s.percentage,
    "grade": lambda s: -s.percentage,
}



@dataclass # dataclass blueprint representing in individual student record
class Student:
    code: str
    name: str
    courseworkMarks: list
    examMark: int

    @property
    def courseworkTotal(self):
        return sum(self.courseworkMarks) # property method to sum coursework marks

    @property
    def totalScore(self):
        return self.courseworkTotal + self.examMark # property method to compute total combined score

    @property
    def percentage(self):
        return self.totalScore / TOTAL_MARKS * 100 # property method to calculate overall percentage score

    @property
    def grade(self):
        return next((grade for cutoff, grade in ((70, "A"), (60, "B"), (50, "C"), (40, "D")) if self.percentage >= cutoff), "F")


def loadStudents(filename):  # funbction to load and parse student records from text file
    with open(filename, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]
    if not lines:
        return [], ["The file is empty."]
    students, warnings = [], []
    try:
        expectedCount = int(lines[0])
    except ValueError:
        expectedCount = None
        warnings.append("The first line should be the number of students.")
    for lineNumber, line in enumerate(lines[1:], start=2):
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 6:
            warnings.append(f"Line {lineNumber}: expected 6 values, found {len(parts)}. Skipped.")
            continue
        try:
            marks, exam = [int(part) for part in parts[2:5]], int(parts[5])
        except ValueError:
            warnings.append(f"Line {lineNumber}: marks must be whole numbers. Skipped.")
            continue
        if not all(0 <= mark <= COURSEWORK_MAX for mark in marks) or not 0 <= exam <= EXAM_MAX:
            warnings.append(f"Line {lineNumber}: a mark is out of range. Skipped.")
            continue
        students.append(Student(parts[0], parts[1], marks, exam))
    if expectedCount is not None and expectedCount != len(students):
        warnings.append(f"The file says {expectedCount} students but {len(students)} were loaded.")
    return students, warnings