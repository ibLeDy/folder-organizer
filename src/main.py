import shutil
import json
import os
from tkinter import filedialog


with open('last_path.txt', 'r') as fp:
    LAST_PATH = fp.read()

with open('formats.json', 'r') as fp:
    EXTENSIONS = json.load(fp)

with open('exclude.txt', 'r') as f:
    EXCLUDE = f.read().strip().splitlines()


def get_path(last_path):
    path = filedialog.askdirectory(initialdir=last_path)
    return path


def save_path(path):
    with open('last_path.txt', 'w') as fp:
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
