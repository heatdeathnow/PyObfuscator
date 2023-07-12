from shutil import copy, copytree
from os import listdir, makedirs
from os.path import join, isdir
import sys


_runtime_imports = ['locale', ]

def _get_modules() -> tuple:
    """
    This function gets a list of all modules imported when loading a program.
    """

    import __main__  # Imports the module which will import all modules used in the program.

    indices = []
    mods = [m for m in sys.modules.keys()]
    for i, mod in enumerate(mods):
        for mod_ in mods:
            if mod_ + '.' in mod:
                indices.append(i)
                break
    
    for i in reversed(indices):
        mods.pop(i)
    mods.pop(mods.index('__main__'))
    if __name__ != '__main__':
        mods.pop(mods.index(__name__))
    
    mods.extend(_runtime_imports)
    return mods


def _get_python_path() -> str:
    """
    Returns the path to Python's installation directory.
    """

    version = ''.join(sys.version.split(' ')[0].split('.')[:-1])  # Gets a three number string according to the version. Python 3.11.4 would be 311.
    for path in sys.path:
        if f'Python{version}' in path[-len(f'Python{version}'):]:
            return path
            break
    
    raise FileNotFoundError("The program was unable to locate Python's installation directory.")


def _from_python_dir(output: str, folder: str) -> None:
    """
    Goes into the specified folder in the PYTHONPATH and copies the modules inside that matches the ones specified in the module list.
    """

    python_path = _get_python_path()
    modules = _get_modules()

    for file in listdir(join(python_path, folder)):
        if isdir(join(python_path, folder, file)) and file in modules:
            try:
                copytree(join(python_path, folder, file), join(join(output, folder, file)))
            except FileNotFoundError:
                makedirs(join(output, folder))
                copytree(join(python_path, folder, file), join(join(output, folder, file)))
            except FileExistsError:
                print('Subdirectory has already been copied to the output directory. Ignoring it.')

        if not isdir(join(python_path, folder, file)) and file.split('.')[0] in modules:  # Sometimes there are files and directories with the same name so `elif` can't be used.
            try:
                copy(join(python_path, folder, file), join(join(output, folder, file)))
            except FileNotFoundError:
                makedirs(join(output, folder))
                copy(join(python_path, folder, file), join(join(output, folder, file)))
            except FileExistsError:
                print('File has already been copied to the output directory. Ignoring it.')

def copy_python(output: str) -> None:
    """
    Copies a Python interpreter with the bare essentials to the output file. This function should be used inside a `setup.py` file which imports the
    project's `main.py` file and `PyToPyc`. If the project uses modules that happen to be imported inside functions and not at the top of the file, then
    there will be a need to update the _runtime_imports parameter located in this module's `__init__.py` file first. If that's not done, the program won't
    be able to tell it's supposed to import those modules as well.
    """

    python_path = _get_python_path()
    files = [file for file in listdir(python_path) if not isdir(join(python_path, file))]
    for file in files:
        try:
            copy(join(python_path, file), join(output, file))
        except FileNotFoundError:
            makedirs(output)
            copy(join(python_path, file), join(output, file))
        except FileExistsError:
            print('File has already been copied to the output directory. Ignoring it.')

    _from_python_dir(output, 'DLLs')
    _from_python_dir(output, 'Lib')
    _from_python_dir(output, 'Tools\\demo')
    _from_python_dir(output, 'Tools\\i18n')
    _from_python_dir(output, 'Tools\\scripts')

    try:
        copytree(join(python_path, 'libs'), join(output, 'libs'))
    except FileNotFoundError:
        makedirs(join(output, 'libs'))
        copytree(join(python_path, 'libs'), join(output, 'libs'))
    except FileExistsError:
        print('Subdirectory has already been copied to the output directory. Ignoring it.')
    
    try:
        copytree(join(python_path, 'Scripts'), join(output, 'Scripts'))
    except FileNotFoundError:
        makedirs(join(output, 'Scripts'))
        copytree(join(python_path, 'Scripts'), join(output, 'Scripts'))
    except FileExistsError:
        print('Subdirectory has already been copied to the output directory. Ignoring it.')
