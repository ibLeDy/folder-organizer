import shutil
import json
import sys
import os
from tkinter import Tk
from tkinter import filedialog
from typing import List
from typing import Dict
from typing import Tuple
from typing import Union
from typing import Optional
from typing import Any


def get_data() -> Tuple[str, Dict[str, str], List[str]]:
    with open(os.path.join(base_path, 'data/last_path.txt'), 'r') as fp:
        last_path: str = fp.read()

    with open(os.path.join(base_path, 'data/formats.json'), 'r') as fp:
        extensions: Dict[str, str] = json.load(fp)

    with open(os.path.join(base_path, 'data/exclude.txt'), 'r') as fp:
        exclude: List[str] = fp.read().strip().splitlines()

    return last_path, extensions, exclude


def get_path(last_path: str) -> Union[Tuple, str]:
    Tk().withdraw()
    path: Union[Tuple, str] = filedialog.askdirectory(initialdir=last_path)
    return path


def save_path(path: str) -> None:
    with open(os.path.join(base_path, 'data/last_path.txt'), 'w') as fp:
        fp.write(path)


def move_file(file: Any, new_path: str) -> None:
    try:
        dst = f'{new_path}/{file.name}'
        shutil.move(file.path, dst)
    except Exception:
        pass


def check_folder(new_path: str) -> None:
    if not os.path.isdir(new_path):
        os.mkdir(new_path)


def check_extension(file: Any):
    _, file_ext = os.path.splitext(file.name)
    for type_, ext in extensions.items():
        if file_ext.lower().strip('.') in ext:
            return type_


if __name__ == '__main__':
    base_path: str = os.path.abspath('.')
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # type: ignore

    last_path, extensions, exclude = get_data()

    # Use path arg if present
    path: Any = get_path(last_path)

    # Continue if user selects a folder
    if path != tuple():

        # List files in directory
        for file in os.scandir(path):

            # Do not move folders and excluded files
            if file.is_file() and file.name not in exclude:

                # If it is a file, correlate its extension
                type_: Optional[str] = check_extension(file)

                # Do not move unknown files
                if not type_:
                    print(f'ERROR Unknown format from file: {file.path !r}')
                else:
                    # Set destination to specific folder
                    new_path: str = f'{path}/{type_}'

                    # Create folder if necessary
                    check_folder(new_path)

                    # Move the file to the new folder
                    move_file(file, new_path)

        # Save last selected path
        save_path(path)
