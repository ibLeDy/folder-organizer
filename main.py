import shutil
import sys
import os


EXCLUDE = ['main.py']
AUDIO = ['ogg']
VIDEO = ['mp4']
IMAGE = ['png']
DOCUMENT = ['pdf']
OTHER = ['py', 'rar']

EXTENSIONS = {
    'Audio': AUDIO,
    'Videos': VIDEO,
    'Images': IMAGE,
    'Documents': DOCUMENT,
    'Other': OTHER,
}


def get_args():
    try:
        path = sys.argv[1]
    except IndexError:
        path = '.'
        print("Directory not specified, using '.'")
    return path


def move_file(file, new_path):
    try:
        dst = f'{new_path}/{file.name}'
        shutil.move(file.path, dst)
    except Exception as e:
        print("[ERROR]", e)


def check_folder(new_path):
    if not os.path.isdir(new_path):
        os.mkdir(new_path)


def check_extension(file):
    file_name, file_ext = file.name.split('.')
    for type_, ext in EXTENSIONS.items():
        if file_ext.lower() in ext:
            return type_


if __name__ == "__main__":
    # Use path arg if present
    path = get_args()

    # List files in directory
    for file in os.scandir(path):

        # Do not move folders and excluded files
        if file.is_file() and file.name not in EXCLUDE:

            # If it is a file, correlate its extension
            type_ = check_extension(file)

            # Do not move unknown files
            if not type_:
                print(f"Unknown format: {file.path !r}")
            else:
                # Set destination to specific folder
                new_path = f'{path}/{type_}'

                # Create folder if necessary
                check_folder(new_path)

                # Move the file to the new folder
                move_file(file, new_path)
