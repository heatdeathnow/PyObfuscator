# PyToPyc
Can recreate a new directory from an input directory exactly like the first one, but with the `.py` files replaced by `.pyc` files.
Can get the modules that are used in your project and copy your Python's installation with the bare-minimum essentials to run your project. It then can create two batch scripts (two `.bat` files) to start your program from the bare-minimum Python interpreter packed inside your distribution file.

## To be done
- Have the packing of the Python interpreter be doable from the command prompt rather than having to create a `setup.py` file. 
- Get a way to figure out all the modules that are imported and those that _could come to be imported_ in the project.
- Organize the package as so to not clutter the IDE with random junk like variables and function that shouldn't show up.

### Python Packing
This can pack a Python distribution inside your program's distribution output folder so that users that do not have Python installed in their computers can run this project.

### Batch scripts
This can create two batch scripts to activate the program in a cleaner way for the end-user.
Ultimately, the distribution folder will have the following subdirectories: Python\ (the packed-in interpreter), bytecode\ (your program's bytecode), start.bat (for starting the program without a prompt), and debug.bat (for starting the program with a prompt).

### Automatic suffix detection
The program automatically detects common suffixes added to the bytecode file names by the Python interpreter. These are:
- .cpython-311
- .cpython-311.opt-1
- .cpython-311.opt-2

If the interpreter used a different suffix for the bytecode file name, then the user can specify it by calling the `--suffix` or `-s` argument.

### Bytecode folder detection
The program is made as to expect the bytecode to always be inside a folder, as is costumary for Python for quite some time now. The default value for this folder is `__pycache__` but it can be specified by calling the `--cache` or the `-c` argument.

### Best way to use PyToPyc
1. Delete all the bytecode from your program.
2. Run your program with the command: `python -OO your_programs_main_file.py`.

This is essential because the interpreter will then create just the necessary bytecode for running the program. There can be situations in which there is more bytecode than necessary (from unused modules and such). Furthermore, by passing the `-OO` argument, docstrings and `assert` statements will not be put in the bytecode, saving space.

3. Run PyToPyc with the following command: `PyToPyc.py your_programs_directory new_directory`.
