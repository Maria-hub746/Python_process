from threading import Thread
from pathlib import Path
import sys
import random
from time import time
import os


TYPE_DICT = {'images' : ('JPEG', 'PNG', 'JPG', 'SVG'),
            'video' : ('AVI', 'MP4', 'MOV', 'MKV'),
            'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLS', 'XLSX', 'PPTX'),
            'audio' : ('MP3', 'OGG', 'WAV', 'AMR'),
            'archives' : ('ZIP', 'GZ', 'TAR'),
            'UFO': ''}

extensions = {}
non_checked_folders = []
sort_with_thread = True

def move_file_to_folder(file):
    #Moves a file according to TYPE_DICT
    extension = Path(file).suffix.split('.')[-1]
    file_name = Path(file).name
    if extension in extensions:
        new_path = Path.joinpath(extensions[extension], file_name)
    else:
        new_path = Path.joinpath(extensions['UFO'], file_name)
    file.rename(new_path)

def sort_files(folder):
    #Sorts files by their extension
    for file in folder.iterdir():
        if sort_with_thread:
            if file.is_dir():
                tread = Thread(target=sort_files, args=(file,))
            else:
                tread = Thread(target=move_file_to_folder, args=(file,))
            tread.run()
        else:
            if file.is_dir():
                sort_files(file)
            else:
                move_file_to_folder(file)

def main():
    path = sys.argv[1]
    if len(sys.argv) < 2:
        raise ValueError('empty path')
    if not (os.path.exists(path) and Path(path).is_dir()):
        raise ValueError('incorrect path')
    folder = Path(path)
    if not folder.is_dir():
        print('Path incorrect')
        exit()

    for key, expansions in TYPE_DICT.items():
        folder_name = Path.joinpath(folder, key)
        folder_name.mkdir(parents=True, exist_ok=True)
        non_checked_folders.append(folder_name)
        for extension in expansions:
            extensions[extension] = folder_name

    folder_name = Path.joinpath(folder, 'UFO')
    extensions['UFO'] = folder_name
    folder_name.mkdir(parents=True, exist_ok=True)
    non_checked_folders.append(folder_name)

    for i in range(5):
        extension = random.choice(list(extensions.keys()))
        if extension == 'UFO':
            file = Path.joinpath(folder, '_' + str(i) + '.xyz')
        else:
            file = Path.joinpath(folder, '_' + str(i) + '.' + extension)
        file.touch(exist_ok=True)

    timer = time()
    sort_files(folder)
    print(f'Done {time() - timer}')


if __name__ == '__main__':
    main()