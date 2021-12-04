import os
import sys
import itertools
import time
import pathlib

here = pathlib.Path(__file__).parent.resolve()
heli_animation_filepath = (here / 'heli_animation.txt')

def clear():
    os.system("cls" if os.name == "nt" else "clear")


with open(heli_animation_filepath, encoding="utf-8") as f:
    helicopter_phases = itertools.cycle(
        [i.strip("\n") for i in filter(None, f.read().split("===================================="))]
    )

def print_heli():
    try:
        for heli_frame in helicopter_phases:
            print(heli_frame)
            print()
            clear()
    except KeyboardInterrupt:
        print("Stopped!")

if __name__ == "__main__":
    print_heli()
    clear()
