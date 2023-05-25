from os.path import isdir, exists, join
from os import mkdir, listdir, rename, remove
from shutil import copy
import shutil
from time import time
import argparse


def rename_bytecode(outdir):  # Removes suffixes from the bytecode files.
    directories = []
    for i in listdir(outdir):
        directory = join(outdir, i)

        if args.suffix in directory:  # If this file contains the suffix in its name, remember it.
            directories.append(directory)

    for file in directories:
        if exists(file) and exists(file.replace(args.suffix, '')):
            print('There are duplicate files. Deleting the one with the suffix...')
            remove(file)
        elif exists(file.replace(args.suffix, '')):
            print('File has already been renamed...')
            pass
        else:
            rename(file, file.replace(args.suffix, ''))  # Removes the suffix, making it so the file has the same name as the original script except for the extension.


def move_misc(indir, outdir):  # Copies miscellaneous files.
    if not exists(outdir):
        mkdir(outdir)

    locations    = []
    destinations = []
    for i in listdir(indir):
        location = join(indir, i)
        destination = join(outdir, i)
        if not isdir(location) and location[-3:] != '.py' and location[-3:] != 'pyc':  # If the file is not a folder and not a Python script, keep its location and create a mirror location for it in the output.
            locations.append(location)
            destinations.append(destination)

    for i in range(len(locations)):
        if exists(destinations[i]):
            print(f'File already exists...')
            pass
        else:
            copytime = time()
            print(f'Copying {locations[i]} to {destinations[i]}...')
            copy(locations[i], destinations[i])
            print(f'Time taken to copy: {time() - copytime:.2f}')


def move_bytecode(indir, outdir):  # Checks if this directory has a bytecode file and, if so, moves all its content to the output file, taking the place of .py files.
    if not exists(outdir):
        mkdir(outdir)

    if exists(join(indir, args.cache)):  # Checks for the bytecode file.
        for file in listdir(join(indir, args.cache)):
            try:
                if exists(join(outdir, file).replace(args.suffix, '')):  # Checks if the a file without the suffix already exists in the output.
                    print(f'The file {file} has already been copied and renamed...')
                    continue
                else:
                    copytime = time()
                    print(f'Copying {file} to {outdir}...')
                    copy(join(indir, args.cache, file), outdir)
                    print(f'Time taken to copy: {time() - copytime:.2f}')
            except shutil.Error:
                pass
        rename_bytecode(outdir)


def recurse(dir):  # Vai entrando de pasta em pasta até não ter mais nada.
    move_bytecode(dir, join(args.output_dir, dir.replace(args.input_dir, '')))
    move_misc(dir, join(args.output_dir, dir.replace(args.input_dir, '')))

    directories = []
    for i in listdir(dir):  # Read the directories from where it is currently at.
        directory = join(dir, i)  # Adds them to the directory it is currently at.
        if isdir(directory) and args.cache not in directory:
            directories.append(directory)  # Keeps them if they're a directory (not a file) and specifically not the bytecode folder.

    if any(isdir(subdir) for subdir in directories):
        for subdir in directories:
            recurse(subdir)  # It will continue this same process until it reaches a folder with no other folders inside, at which point it continues from the directory immediately before it had gotten into this one.


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='PyObfuscator',
                                     description='Takes in a Python project directory and copies all the bytecodes and non-py files to an output directory.',
                                     epilog='Visit my Github: heatdeathnow')

    parser.add_argument('input_dir', help='The path to your Python code.')
    parser.add_argument('output_dir', help='Where a copy of the input directory will be created and the bytecode and other files dumped.')
    parser.add_argument('-s', '--suffix', default='.cpython-311', help='The part of the name of the bytecode files which will be removed. The default is .cpython-311')
    parser.add_argument('-c', '--cache', type=str, default='__pycache__', help='The name of the folder where the Python interpreter has stored all the bytecode.')

    args = parser.parse_args()

    try:
        mkdir(args.output_dir)  # Creates the output directory
    except FileExistsError:
        pass

    recurse(args.input_dir)
