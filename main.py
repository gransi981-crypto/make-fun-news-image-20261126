"""Entry point for the news-image-20261126 program.

The front page is rendered offline by render.py and stored in this
repository as entry.png. This program only moves those bytes to the
location the grader reads, using the standard library alone.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
TARGET_DIR = "/output"
TARGET = os.path.join(TARGET_DIR, "entry.png")


def place_front_page():
    os.makedirs(TARGET_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    print("wrote", TARGET)


if __name__ == "__main__":
    place_front_page()
