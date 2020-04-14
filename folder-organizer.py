import shutil
import json
import sys
import os
from tkinter import filedialog


try:
    BASE_PATH = sys._MEIPASS
except AttributeError:
    BASE_PATH = os.path.abspath('.')

with open(os.path.join(BASE_PATH, 'data/last_path.txt'), 'r') as fp:
    LAST_PATH = fp.read()

with open(os.path.join(BASE_PATH, 'data/formats.json'), 'r') as fp:
    EXTENSIONS = json.load(fp)

with open(os.path.join(BASE_PATH, 'data/exclude.txt'), 'r') as f:
    EXCLUDE = f.read().strip().splitlines()


def get_path(last_path):
    path = filedialog.askdirectory(initialdir=last_path)
    return path


def save_path(path):
    with open(os.path.join(BASE_PATH, 'data/last_path.txt'), 'w') as fp:
        fp.write(path)


def move_file(file, new_path):
    try:
        dst = f'{new_path}/{file.name}'
        shutil.move(file.path, dst)
        print(f'Moved {file.name} to {new_path}')
    except Exception as e:
        print('[ERROR]', e)


def check_folder(new_path):
    if not os.path.isdir(new_path):
        os.mkdir(new_path)


def check_extension(file):
    file_name, file_ext = os.path.splitext(file.name)
    for type_, ext in EXTENSIONS.items():
        if file_ext.lower().strip('.') in ext:
            return type_


if __name__ == '__main__':
    # Use path arg if present
    path = get_path(LAST_PATH)

    # Continue if user selects a folder
    if path != tuple():

        # List files in directory
        for file in os.scandir(path):

            # Do not move folders and excluded files
            if file.is_file() and file.name not in EXCLUDE:

                # If it is a file, correlate its extension
                type_ = check_extension(file)

                # Do not move unknown files
                if not type_:
                    print(f'ERROR Unknown format from file: {file.path !r}')
                else:
                    # Set destination to specific folder
                    new_path = f'{path}/{type_}'

                    # Create folder if necessary
                    check_folder(new_path)

                    # Move the file to the new folder
                    move_file(file, new_path)

        # Save last selected path
        save_path(path)
