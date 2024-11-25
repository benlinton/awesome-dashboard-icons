#!/usr/bin/python3

from pathlib import Path
import os
import re

def unique_count(dir):
    files = Path(dir).glob("*.*g")
    unique = list({os.path.splitext(file)[0] for file in files})
    return len(unique)

def update_count(file_path, icons_path):
    with open(file_path, "r") as file:
        content = file.read()
    updated_content = re.sub(r"\d+ icon", f'{unique_count(icons_path)} icon', content)
    with open(file_path, "w") as file:
        file.write(updated_content)

if __name__ == "__main__":
    update_count("README.md", "./icons")
