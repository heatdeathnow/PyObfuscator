from os import mkdir, listdir, rename, remove
from os.path import isdir, exists, join
from shutil import copy
from time import time
import argparse

"""
This program does not compile the code into bytecode by itself. If it were to use something like compile_dir, it would compile every single piece of Python code on that directory.
However, that is not necessary. When you import a module or package into your virtual environment, not all of its parts are used. If the program were to do that, it would bloat the
bytecode unnecessarily. Another option, which I considered, would have been to copy all non-.py and non-.pyc files into the new directory first and then compile all files which have
a bytecode equivalent (meaning they have been previously imported by the source code and therefore won't just sit there doing nothing) with optimization 2. This would remove all
docstrings and assert statements, which some modules and packages tend to have and that would just weight the final program down. I didn't go for this option because I thought it
would be redundant. It may happen that you changed your program and some modules are no longer used, this approach would compile them anyways; besides, this would imply the addition
of two modes for this module, one in which it just moves the bytecode with no compilation, and one in which it compiles it based on the possibly flawed assumption that all the would-be
corresponding bytecode was being used.

The way I recommend using this program is as follows: go into your source code directory; search for all the __pycache__ files (or whatever you might have them configure to be called),
and delete them; run your program with the -OO parameter (such as: python -OO your_program_name.py); close it and finally run this module like the following:
PyToPyc.py source_code_directory output_directory
"""


def rename_bytecode(outdir):  # Removes suffixes from the bytecode files.
    global used_suffix
    for i in listdir(outdir):
        if i[-4:] == '.pyc':
            file = join(outdir, i)

            if exists(file) and exists(file.replace(used_suffix, '')):
                print(f'Duplicates found, removing the one that still has its suffix.')
                remove(file)

            elif exists(file.replace(used_suffix, '')):
                print('File has already been renamed...')

            else:
                rename(file, file.replace(used_suffix, ''))  # Removes the suffix, making it so the file has the same name as the original script except for the extension.


def move_misc(indir, outdir):  # Copies miscellaneous files.
    if not exists(outdir):
        mkdir(outdir)

    for i in listdir(indir):
        location = join(indir, i)
        destination = join(outdir, i)
        if not isdir(location) and location[-3:] != '.py' and location[
                                                              -4:] != '.pyc':  # If the file isn't a folder, isn't a Python script and isn't bytecode, keep its location and create a mirror location for it in the output.
            if exists(destination):  # If you try to copy a file that is already there, you will get a ShutilError.
                print(f'File {destination} already exists...')
                pass

            else:
                copytime = time()
                print(f'Copying {location} to {destination}...')
                copy(location, destination)
                try:
                    print(f'Time taken to copy: {time() - copytime:.2f} seconds.')
                except ZeroDivisionError:
                    print(f'Time taken to copy: 0 seconds.')


def move_bytecode(indir, outdir):  # Checks if this directory has a bytecode file and, if so, moves all its content to the output file, taking the place of .py files.
    global used_suffix
    if not exists(outdir):
        mkdir(outdir)

    if exists(join(indir, args.cache)):  # Checks for the bytecode file.
        for file in listdir(join(indir, args.cache)):

            i = 0
            while used_suffix is None:
                try:
                    if suffixes[i] in str(file):
                        used_suffix = suffixes[i]
                    i += 1
                except IndexError:
                    raise Exception(f'No suffix was passed and the program was unable to match the file {file} with any '
                                    f'of the corresponding suffixes: {[suffix for suffix in suffixes]}')

            if args.suffix is not None and used_suffix not in file:
                raise Exception(f'The program was unable to match the user passed suffix {args.suffix} with the file {file}.')

            elif used_suffix not in file:
                raise Exception(f'The program had previously matched the default suffix {used_suffix} with a file, '
                                f'however, it was now unable to match it with the file {file}.')

            elif exists(join(outdir, file).replace(used_suffix, '')):  # Checks if the file without the suffix already exists in the output.
                print(f'The file {file} has already been copied and renamed...')

            elif exists(join(outdir, file)):
                print(f'The file {file} has already been copied...')

            else:
                copytime = time()
                print(f'Copying {file} to {outdir}...')
                copy(join(indir, args.cache, file), outdir)
                print(f'Time taken to copy: {time() - copytime:.2f}')

        rename_bytecode(outdir)


def recurse_copy(
        recdir):  # Enters each folder until its very end, ignoring all others. Only after reaching and end does it go for the next subfolders.
    move_bytecode(recdir, join(args.output_dir, recdir.replace(args.input_dir, '')))
    move_misc(recdir, join(args.output_dir, recdir.replace(args.input_dir, '')))

    for i in listdir(recdir):  # Reads the directories from where it is currently at.
        directory = join(recdir, i)  # Adds them to the directory it is currently at.

        if isdir(
                directory) and args.cache not in directory and directory != recdir:  # If it's a directory, and not the bytecode directory, and it's different from the original...
            recurse_copy(directory)


if __name__ == '__main__':
    runtime = time()
    suffixes = ('.cpython-311.opt-2', '.cpython-311.opt-1', '.cpython-311')
    used_suffix = None

    parser = argparse.ArgumentParser(prog='PyToPyc',
                                     description='Takes in a Python project directory and copies all the bytecodes and non-py files to an output directory.',
                                     epilog='Visit my GitHub: heatdeathnow')

    parser.add_argument('input_dir', help='The path to your Python code.')
    parser.add_argument('output_dir',
                        help='Where a copy of the input directory will be created and the bytecode and other files dumped.')
    parser.add_argument('-s', '--suffix', type=str,
                        help="The part of the bytecode files' name to be removed. The program already identifies the standard suffix names automatically, but if the suffixes do not follow "
                             "the standard, they can be specified with this argument.")
    parser.add_argument('-c', '--cache', type=str, default='__pycache__',
                        help='The name of the folder where the Python interpreter has stored all the bytecode. The default is __pycache__')

    args = parser.parse_args()
    args.input_dir = args.input_dir.replace('/', '\\')
    args.output_dir = args.output_dir.replace('/', '\\')

    if args.input_dir[-1] != '\\':
        args.input_dir += '\\'
    if args.output_dir[-1] != '\\':
        args.output_dir += '\\'

    # Start of the program
    used_suffix = args.suffix

    try:
        mkdir(args.output_dir)  # Creates the output directory
    except FileExistsError:
        pass

    recurse_copy(args.input_dir)

    try:
        print(f'Total runtime: {time() - runtime:.2f} seconds.')
    except ZeroDivisionError:
        print(f'Total runtime: 0 seconds.')
