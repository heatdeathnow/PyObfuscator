from os.path import isdir, exists, join, normpath, basename, abspath
from os import mkdir, listdir, rename, remove, getcwd
from argparse import ArgumentParser
from compileall import compile_dir
from shutil import copy, rmtree
from time import perf_counter
from sys import version_info

"""
### This program will do the following:
 - Remove all the bytecode from the input directory.
 - Compile every single `.py` file with optimization level two (-OO).
 - It will then copy every single `non-.py` file to the output directory, recreating the subfolders of the original.
 - In this process, it will rename every single `.pyc` file to its corresponding `.py` file's name.
 - After everything has been copied over the program will then create two batch (`.bat`) files:
 - The `start.bat` file will initiate the passed program's `main.py` file or similar without the console and pass to it every argument passed to the batch file.
 - The `debug.bat` file will do the same, but it will open the console and prevent it from closing automatically after the program is terminated.

In essence, this program "compiles" the passed program to Python's bytecode, offering a layer of obfuscation and reducing the size of the passed program.
The "compiled" program can then be distributed to other machines, as long as they have a Python interpreter.
"""

def _bytecide(dir: str, cache: str = '__pycache__') -> None:
    """
    Goes through this directory tree and wipes out subdirectories whose name equals the cache variable.
    The default value for the cache parameter is `__pycache__`.
    """

    dirs = [dir_ for dir_ in listdir(dir) if isdir(join(dir, dir_))]
    for subdir in dirs:
        if subdir == cache:
            rmtree(join(dir, subdir))
        else:
            _bytecide(join(dir, subdir))


def _rename_bytecode(outdir: str) -> None:
    """
    Removes the suffixes from the names of the bytecode files;
    makes them the same name as the original source code file if not for the `.pyc` instead of `.py`.
    """

    for i in listdir(outdir):
        if i[-4:] == '.pyc':
            file = join(outdir, i)

            if exists(file) and exists(file.replace(_suffix, '')):
                if _is_main: print(f'Duplicates found, removing the one that still has its suffix.')
                remove(file)

            elif exists(file.replace(_suffix, '')):
                if _is_main: print('File has already been renamed...')
                pass

            else:
                rename(file, file.replace(_suffix, ''))  # Removes the suffix, making it so the file has the same name as the original script except for the extension.


def _move_misc(indir: str, outdir: str) -> None:
    """
    Copies miscellaneous files in the input directory to its mirror location in the output directory.
    """

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
                copytime = perf_counter()
                if _is_main: print(f'Copying {location} to {destination}...')
                copy(location, destination)
                try:
                    if _is_main: print(f'Time taken to copy: {perf_counter() - copytime:.2f} seconds.')
                    pass
                except ZeroDivisionError:
                    if _is_main: print(f'Time taken to copy: 0 seconds.')
                    pass


def _move_bytecode(indir: str, outdir: str) -> None:
    """
    Checks if this directory has a bytecode file and, if so, moves all its content to the output file, taking the place of `.py` files.
    """

    if not exists(outdir):
        mkdir(outdir)

    if exists(join(indir, _cache)):  # Checks for the bytecode file.
        for file in listdir(join(indir, _cache)):
            if exists(join(outdir, file).replace(_suffix, '')):  # Checks if the file without the suffix already exists in the output.
                if _is_main: print(f'The file {file} has already been copied and renamed...')
                pass

            elif exists(join(outdir, file)):
                if _is_main: print(f'The file {file} has already been copied...')
                pass

            else:
                copytime = perf_counter()
                if _is_main: print(f'Copying {file} to {outdir}...')
                copy(join(indir, _cache, file), outdir)
                if _is_main: print(f'Time taken to copy: {perf_counter() - copytime:.2f}')
        _rename_bytecode(outdir)


def _recurse_copy(input_: str, indir: str, outdir: str) -> None:
    """
    This function enters each path until its very end while activating the `_move_bytecode` and `_move_misc` functions. It will ignore all the other possible
    paths it could have taken until it reaches a dead-end. After reaching a dead-end, it will return one folder and go the next fork, if one is
    available, if not it will return one more and so on.
    """
    
    _move_bytecode(indir, join(outdir, indir.replace(input_, '')))
    _move_misc(indir, join(outdir, indir.replace(input_, '')))

    for i in listdir(indir):  # Reads the directories from where it is currently at.
        directory = join(indir, i)  # Adds them to the directory it is currently at.

        if isdir(directory) and _cache not in directory and directory != indir:  # If it's a directory, and not the bytecode directory, and it's different from the original...
            _recurse_copy(input_, directory, outdir)


def _fix_slash(path: str) -> str:
    r"""
    Replaces forward slashes with backslashes in a path. If the argument passed doesn't end in either slashes, this function will add a backslash to it.
    """

    x = path.replace('/', '\\')
    if x[-1] != '\\':
        x += '\\'

    return x


def tobytecode(directory: str, output: str = None, cache: str = None) -> None:
    """
    This functions goes through an entire Python project's directory and copies all the files to the output, excep the
    source code (`.py` files) which it leaves behind, putting the bytecode (`.pyc` files) in its would-be place.

    Parameters:

    directory - The path to the Python project.

    output    - The path to where the program should dump the bytecode-compiled project. Default is the original name
                plus " - bytecode".

    cache     - What the IDE has named the files that contain the bytecode. Default is "__pycache__".
    """

    global _cache

    if output is None:
        output = basename(normpath(directory)) + ' - bytecode\\'

    if cache is not None:
        _cache = cache

    try:
        mkdir(output)
    except FileExistsError:
        pass

    _recurse_copy(_fix_slash(directory), _fix_slash(directory), _fix_slash(output))


_cache = '__pycache__'
_is_main = False
_suffix = f'.cpython-{version_info.major}{version_info.minor}.opt-2'
if __name__ == '__main__':
    # So that the other modules know that this is being run as the main program, and not as a package.
    _is_main = True
    runtime = perf_counter()

    parser = ArgumentParser(prog='PyToPyc',
                            description='Takes in a Python project directory and copies all the bytecodes and non-py files to an output directory.',
                            epilog='Visit my GitHub: heatdeathnow')
    parser.add_argument('input', help='The path to your Python code.')
    parser.add_argument('-o', '--output', type=str,
                        help='Where a copy of the input directory will be created and the bytecode and other files dumped. Default is "bytecode\\"')
    parser.add_argument('-s', '--suffix', type=str,
                        help=f"The part of the bytecode files' name to be removed. The program already identifies the standard suffix name for maximum \
                        optimization automatically, but if your suffix doesn't follow the standard, it can be specified with this argument. Defaults \
                        to the corresponding -OO suffix for your Python version. Yours is {_suffix}")
    parser.add_argument('-c', '--cache', type=str, default='__pycache__',
                        help='The name of the folder where the Python interpreter has stored all the bytecode. The default is __pycache__')
    parser.add_argument('-n', '--name', type=str, default='main',
                        help="The name of the program's main file.")
    args = parser.parse_args()

    _cache = args.cache
    
    args.input = _fix_slash(args.input)
    if abspath(args.input) == getcwd():
        raise PermissionError('Do not pass the working directory as an input. Either move this module outside your project or put your project \
                              inside a subdirectory')

    if args.output is None:
        args.output = normpath(args.input) + ' - bytecode\\'
    else:
        args.output = _fix_slash(args.output)

    # Start of the program
    try:
        mkdir(args.output)  # Creates the output directory. If the interpreter option was not activated, it is necessary to create the output here.
    except FileExistsError:
        pass

    _bytecide(args.input)
    compile_dir(args.input, optimize=2)
    _recurse_copy(args.input, args.input, args.output)

    start_script = f'@ECHO OFF\nstart pythonw -OO "%~dp0{args.name}.pyc" %*\n'
    debug_script = f'@ECHO ON\npython -OO "%~dp0{args.name}.pyc" %*\npause\n'

    try:
        with open(join(args.output, 'start.bat'), 'x') as file: file.write(start_script)
    except FileExistsError:
        with open(join(args.output, 'start.bat'), 'w') as file: file.write(start_script)

    try:
        with open(join(args.output, 'debug.bat'), 'x') as file: file.write(debug_script)
    except FileExistsError:
        with open(join(args.output, 'debug.bat'), 'w') as file: file.write(debug_script)    

    try:
        print(f'Total runtime: {perf_counter() - runtime:.2f} seconds.')
        pass
    except ZeroDivisionError:
        print(f'Total runtime: 0.00 seconds.')
        pass
