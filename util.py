import os
import time
from typing import List

start_time = time.time()


def save_to_file(content: List[str], filename):
    if not os.path.exists(filename):
        with open(filename, "w") as file:
            file.write("")
    try:
        with open(filename, "a+") as file:
            for line in content:
                file.write(line + "\n")
    except:
        pass


def read_file(filename):
    with open(filename, "r") as file:
        return [s[:-1] for s in file.readlines()]


def time_passed():
    # format time passed in seconds to hh:mm:ss
    seconds = time.time() - start_time
    hours = int(seconds // 3600)
    seconds -= hours * 3600
    minutes = int(seconds // 60)
    seconds -= minutes * 60
    return f'{hours}:{minutes}:{int(seconds)}'
