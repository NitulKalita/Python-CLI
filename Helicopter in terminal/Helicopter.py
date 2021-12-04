import os
import sys
import itertools
import time


def clear():
    os.system("cls" if os.name == "nt" else "clear")


with open("heli_animation.txt", encoding="utf-8") as f:
    helicopter_phases = itertools.cycle(
        [i.strip("\n") for i in filter(None, f.read().split("===================================="))]
    )

def print_heli():
    try:
        for heli_frame in helicopter_phases:
            print(heli_frame)
            time.sleep(float(sys.argv[1]) if sys.argv[1:] else 0.1)
            clear()
    except KeyboardInterrupt:
        print("Stopped!")

if __name__ == "__main__":
    print_heli()
    clear()
