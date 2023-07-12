from os.path import basename, normpath, join, abspath, exists
from argparse import ArgumentParser
from time import perf_counter
from os import mkdir, getcwd
from compileall import compile_dir
import moduletools
import bytecode
from shutil import rmtree
from sys import argv


if __name__ == '__main__':
    bytecode._is_main = True
    runtime = perf_counter()

    parser = ArgumentParser(prog='PyToPyc',
                            description='Takes in a Python project directory and copies all the bytecodes and non-py files to an output directory.',
                            epilog='Visit my GitHub: heatdeathnow')

    parser.add_argument('input', help='The path to your Python code.')
    parser.add_argument('-i', '--interpreter', action='store_true',
                        help='Should the program pack a striped-down Python interpreter with the bytecode? Default is False.')
    parser.add_argument('-n', '--name', required='--interpreter' in argv or '-i' in argv,
                        help="The name of your program's `main.py` file (case sensitive).This argument is required if the --interpreter/-i option \
                        is active.")
    parser.add_argument('-o', '--output', type=str,
                        help='Where a copy of the input directory will be created and the bytecode and other files dumped. Default is "bytecode\\"')
    parser.add_argument('-s', '--suffix', type=str,
                        help="The part of the bytecode files' name to be removed. The program already identifies the standard suffix names \
                        automatically, but if the _suffixes do not follow the standard, they can be specified with this argument.")
    parser.add_argument('-c', '--cache', type=str, default='__pycache__',
                        help='The name of the folder where the Python interpreter has stored all the bytecode. The default is __pycache__')

    args = parser.parse_args()

    bytecode._user_suffix = args.suffix
    bytecode._cache = args.cache
    
    args.input = bytecode._fix_slash(args.input)
    if abspath(args.input) == getcwd():
        raise PermissionError('Do not pass the working directory as an input. Either move this module outside your project or put your project \
                              inside a subdirectory')

    if args.name[-3:].lower() == '.py': 
        args.name = args.name.replace('.py', '')
    if not exists(join(args.input, f'{args.name}.py')):
        raise ValueError(f'PyToPyc was unable to find {join(args.input, args.name)}\nKeep in mind the names are case sensitive.')

    if args.output is None:
        args.output = basename(normpath(args.input)) + ' - bytecode\\'
    else:
        args.output = bytecode._fix_slash(args.output)

    # Start of the program
    if args.interpreter:
        moduletools.copy_python(join(args.output, 'pytopyc_tmp\\'))
        bytecode._bytecide(join(args.output, 'pytopyc_tmp\\'), bytecode._cache)
        compile_dir(join(args.output, 'pytopyc_tmp\\'), optimize=2)
        bytecode._recurse_copy(join(args.output, 'pytopyc_tmp\\'), join(args.output, 'pytopyc_tmp\\'), join(args.output, 'Python\\'))
        rmtree(join(args.output, 'pytopyc_tmp\\'))

    bytecode._used_suffix = bytecode._user_suffix
    try:
        mkdir(args.output)  # Creates the output directory. If the interpreter option was not activated, it is necessary to create the output here.
    except FileExistsError:
        pass
    
    if args.interpreter:
        start_script = f'@ECHO OFF\ncd bytecode\\\nstart pythonw -OO {args.name}.pyc %*\n'
        debug_script = f'@ECHO ON\ncd bytecode\\\npython -OO {args.name}.pyc %*\npause\n'
        bytecode._recurse_copy(args.input, args.input, join(args.output, 'bytecode'))

        try:
            with open(join(args.output, 'start.bat'), 'x') as file: file.write(start_script)
        except FileExistsError:
            with open(join(args.output, 'start.bat'), 'w') as file: file.write(start_script)

        try:
            with open(join(args.output, 'debug.bat'), 'x') as file: file.write(debug_script)
        except FileExistsError:
            with open(join(args.output, 'debug.bat'), 'w') as file: file.write(debug_script)    
    else:
        bytecode._recurse_copy(args.input, args.input, args.output)

    try:
        print(f'Total runtime: {perf_counter() - runtime:.2f} seconds.')
        pass
    except ZeroDivisionError:
        print(f'Total runtime: 0 seconds.')
        pass
