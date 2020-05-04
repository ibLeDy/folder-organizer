import shutil
import json
import sys
import os
from tkinter import Tk
from tkinter import filedialog


def get_data():
    with open(os.path.join(base_path, 'data/last_path.txt'), 'r') as fp:
        last_path = fp.read()

    with open(os.path.join(base_path, 'data/formats.json'), 'r') as fp:
        extensions = json.load(fp)

    with open(os.path.join(base_path, 'data/exclude.txt'), 'r') as fp:
        exclude = fp.read().strip().splitlines()

    return last_path, extensions, exclude


def get_path(last_path):
    Tk().withdraw()
    path = filedialog.askdirectory(initialdir=last_path)
    return path


def save_path(path):
    with open(os.path.join(base_path, 'data/last_path.txt'), 'w') as fp:
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
    _, file_ext = os.path.splitext(file.name)
    for type_, ext in extensions.items():
        if file_ext.lower().strip('.') in ext:
            return type_


if __name__ == '__main__':
    base_path = os.path.abspath('.')
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # type: ignore

    last_path, extensions, exclude = get_data()

    path = get_path(last_path)
    if path != tuple():
        for file in os.scandir(path):
            if file.is_file() and file.name not in exclude:
                type_ = check_extension(file)
                if type_:
                    new_path = f'{path}/{type_}'
                    check_folder(new_path)
                    move_file(file, new_path)

        save_path(path)
