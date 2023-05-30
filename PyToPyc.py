from os import mkdir, listdir, rename, remove
from shutil import Error as ShutilError
from os.path import isdir, exists, join
from shutil import copy
from time import time
import argparse


'''
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
PyToPyc.py source_code_directory output_directory -s .cpython-311.opt-2
'''


def rename_bytecode(outdir):  # Removes suffixes from the bytecode files.
    for i in listdir(outdir):
        file = join(outdir, i)

        if args.suffix in file:  # If this file contains the suffix in its name...
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

    for i in listdir(indir):
        location = join(indir, i)
        destination = join(outdir, i)
        if not isdir(location) and location[-3:] != '.py' and location[-3:] != 'pyc':  # If the file isn't a folder, isn't a Python script and isn't bytecode, keep its location and create a mirror location for it in the output.
            if exists(destination):
                print(f'File already exists...')
                pass
            else:
                copytime = time()
                print(f'Copying {location} to {destination}...')
                copy(location, destination)
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
            except ShutilError:
                pass
        rename_bytecode(outdir)


def recurse_copy(recdir):  # Enters each folder until its very, ignoring all others. Only after reaching and end, it goes for the next subfolders.
    move_bytecode(recdir, join(args.output_dir, recdir.replace(args.input_dir, '')))
    move_misc(recdir, join(args.output_dir, recdir.replace(args.input_dir, '')))

    for i in listdir(recdir):  # Read the directories from where it is currently at.
        directory = join(recdir, i)  # Adds them to the directory it is currently at.
        if isdir(directory) and args.cache not in directory and directory != recdir:  # If it's a directory, and not the bytecode directory, and it's different from the original...
            recurse_copy(directory)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='PyObfuscator',
                                     description='Takes in a Python project directory and copies all the bytecodes and non-py files to an output directory.',
                                     epilog='Visit my Github: heatdeathnow')

    parser.add_argument('input_dir', help='The path to your Python code.')
    parser.add_argument('output_dir', help='Where a copy of the input directory will be created and the bytecode and other files dumped.')
    parser.add_argument('-s', '--suffix', default='.cpython-311', help='The part of the name of the bytecode files which will be removed. The default is .cpython-311')
    parser.add_argument('-c', '--cache', type=str, default='__pycache__', help='The name of the folder where the Python interpreter has stored all the bytecode.')

    args = parser.parse_args()

    if args.input_dir[-1] != '/' or args.input_dir[-1] != '\\':
        args.input_dir += '/'
    if args.output_dir[-1] != '/' or args.output_dir[-1] != '\\':
        args.output_dir += '/'

    # Start of the program
    try:
        mkdir(args.output_dir)  # Creates the output directory
    except FileExistsError:
        pass

    recurse_copy(args.input_dir)
