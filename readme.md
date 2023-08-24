# PyToPyc
In essence, this program "compiles" the passed program to Python's bytecode, offering a layer of obfuscation and reducing the size of the passed program. The "compiled" program can then be distributed to other machines, as long as they have a Python interpreter. All that is necessary to do at this point is to create a shortcut of the `start.bat` file and move it to the user's desktop.

### Batch scripts
PyToPyc creates two batch scripts to activate the program in a cleaner way for the end-user. `start.bat` activates the program without the Python console and `debug.bat` activates the program with the Python console and holds it open until manually closed.

### Overview of accepted arguments
PyToPyc can be used using only one argument: the directory to your project. But it also accepts several other optional arguments. These are listed below.
 - `-o` or `--output` then "path-to-your-project"	Specify the directory which should be created and compiled to.
 - `-s` or `--suffix` then "example.cpython.331.2"	Specify the suffix that your interpreter is adding to the bytecode files. Defaults to the -OO suffix for your Python version. If you're using Python 3.11.4, for example, it would be .cpython-311.opt-2
 - `-c` or `--cache` then "bytecode_files_dirs"		Specify the name of the folders that your interpreter creates to store the bytecode files. Use "." if it uses no folder.
 - `-n` or `--name` then "your_programs_main_file	Specify the name of your program's main file. This is the file which activated the rest of the program. Default is "main.py"
