from os import mkdir, listdir, rename, remove
from os.path import isdir, exists, join, normpath, basename
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
PyToPyc.py source_code_directory outputectory
"""


def _rename_bytecode(outdir):  # Removes _suffixes from the bytecode files.
    global _used_suffix
    for i in listdir(outdir):
        if i[-4:] == '.pyc':
            file = join(outdir, i)

            if exists(file) and exists(file.replace(_used_suffix, '')):
                if _is_main: print(f'Duplicates found, removing the one that still has its suffix.')
                remove(file)

            elif exists(file.replace(_used_suffix, '')):
                if _is_main: print('File has already been renamed...')
                pass

            else:
                rename(file, file.replace(_used_suffix, ''))  # Removes the suffix, making it so the file has the same name as the original script except for the extension.


def _move_misc(indir, outdir):  # Copies miscellaneous files.
    if not exists(outdir):
        mkdir(outdir)

    for i in listdir(indir):
        location = join(indir, i)
        destination = join(outdir, i)

        if not isdir(location) and location[-3:] != '.py' and location[-4:] != '.pyc':  # If the file isn't a folder, isn't a Python script and isn't bytecode, keep its location and create a mirror location for it in the output.
            if exists(destination):  # If you try to copy a file that is already there, you will get a ShutilError.
                if _is_main: print(f'File {destination} already exists...')
                pass

            else:
                copytime = time()
                if _is_main: print(f'Copying {location} to {destination}...')
                copy(location, destination)
                try:
                    if _is_main: print(f'Time taken to copy: {time() - copytime:.2f} seconds.')
                    pass
                except ZeroDivisionError:
                    if _is_main: print(f'Time taken to copy: 0 seconds.')
                    pass


def _move_bytecode(indir, outdir):  # Checks if this directory has a bytecode file and, if so, moves all its content to the output file, taking the place of .py files.
    global _used_suffix, _suffixes
    if not exists(outdir):
        mkdir(outdir)

    if exists(join(indir, _cache)):  # Checks for the bytecode file.
        for file in listdir(join(indir, _cache)):

            i = 0
            while _used_suffix is None:
                try:
                    if _suffixes[i] in str(file):
                        _used_suffix = _suffixes[i]
                    i += 1
                except IndexError:
                    raise Exception(f'No suffix was passed and the program was unable to match the file {file} with any '
                                    f'of the corresponding _suffixes: {[suffix for suffix in _suffixes]}')

            if _user_suffix is not None and _used_suffix not in file:
                raise Exception(f'The program was unable to match the user passed suffix {_user_suffix} with the file {file}.')

            elif _used_suffix not in file:
                raise Exception(f'The program had previously matched the default suffix {_used_suffix} with a file, '
                                f'however, it was now unable to match it with the file {file}.')

            elif exists(join(outdir, file).replace(_used_suffix, '')):  # Checks if the file without the suffix already exists in the output.
                if _is_main: print(f'The file {file} has already been copied and renamed...')
                pass

            elif exists(join(outdir, file)):
                if _is_main: print(f'The file {file} has already been copied...')
                pass

            else:
                copytime = time()
                if _is_main: print(f'Copying {file} to {outdir}...')
                copy(join(indir, _cache, file), outdir)
                if _is_main: print(f'Time taken to copy: {time() - copytime:.2f}')

        _rename_bytecode(outdir)


def _recurse_copy(input_, indir, outdir):  # Enters each folder until its very end, ignoring all others. Only after reaching and end does it go for the next subfolders.
    _move_bytecode(indir, join(outdir, indir.replace(input_, '')))
    _move_misc(indir, join(outdir, indir.replace(input_, '')))

    for i in listdir(indir):  # Reads the directories from where it is currently at.
        directory = join(indir, i)  # Adds them to the directory it is currently at.

        if isdir(directory) and _cache not in directory and directory != indir:  # If it's a directory, and not the bytecode directory, and it's different from the original...
            _recurse_copy(input_, directory, outdir)


def _fix_slash(path):
    x = path.replace('/', '\\')
    if x[-1] != '\\':
        x += '\\'

    return x


def to_bytecode(directory, output=None, cache=None, suffix=None):
    """
    This functions goes through an entire Python project's directory and copies all the files to the output, excep the
    source code (.py files) which it leaves behind, putting the bytecode (.pyc files) in its would-be place.

    Arguments:

    directory - The path to the Python project.
    output    - The path to where the program should dump the bytecode-compiled project. Default is the original name
                plus " - bytecode".
    cache     - What the IDE has named the files that contain the bytecode. Default is "__pycache__".
    suffix    - The string the interpreter concatenates to the bytecode files' names. If nothing is passed, the program
                will attempt to match the following suffixes ".cpython-311.opt-2", ".cpython-311.opt-1", ".cpython-311"
                to the file names.
    """

    global _cache, _user_suffix, _used_suffix

    if output is None:
        output = basename(normpath(directory)) + ' - bytecode\\'

    if cache is not None:
        _cache = cache

    if suffix is not None:
        _user_suffix = suffix
        _used_suffix = _user_suffix

    try:
        mkdir(output)
    except FileExistsError:
        pass

    _recurse_copy(_fix_slash(directory), _fix_slash(directory), _fix_slash(output))


# "Private" variables used by this program.
_suffixes = ('.cpython-311.opt-2', '.cpython-311.opt-1', '.cpython-311')
_used_suffix = None
_user_suffix = None
_cache = '__pycache__'
_is_main = False


if __name__ == '__main__':
    _is_main = True
    runtime = time()

    parser = argparse.ArgumentParser(prog='PyToPyc',
                                     description='Takes in a Python project directory and copies all the bytecodes and non-py files to an output directory.',
                                     epilog='Visit my GitHub: heatdeathnow')

    parser.add_argument('input', help='The path to your Python code.')
    parser.add_argument('-o', '--output', type=str,
                        help='Where a copy of the input directory will be created and the bytecode and other files dumped. Default is "bytecode\\"')
    parser.add_argument('-s', '--suffix', type=str,
                        help="The part of the bytecode files' name to be removed. The program already identifies the standard suffix names automatically, but if the _suffixes do not follow "
                             "the standard, they can be specified with this argument.")
    parser.add_argument('-c', '--cache', type=str, default='__pycache__',
                        help='The name of the folder where the Python interpreter has stored all the bytecode. The default is __pycache__')

    args = parser.parse_args()
    _user_suffix = args.suffix
    _cache = args.cache

    args.input = _fix_slash(args.input)

    if args.output is None:
        args.output = basename(normpath(args.input)) + ' - bytecode\\'
    else:
        args.output = _fix_slash(args.output)

    # Start of the program
    _used_suffix = _user_suffix

    try:
        mkdir(args.output)  # Creates the output directory
    except FileExistsError:
        pass

    _recurse_copy(args.input, args.input, args.output)

    try:
        print(f'Total runtime: {time() - runtime:.2f} seconds.')
        pass
    except ZeroDivisionError:
        print(f'Total runtime: 0 seconds.')
        pass
