# PyToPyc
Creates a new directory from an input directory exactly like the first one, but with the `.py` files replaced by `.pyc` files.

### Automatic suffix detection
The program automatically detects common suffixes added to the bytecode file names by the Python interpreter. These are:
* .cpython-311
* .cpython-311.opt-1
* .cpython-311.opt-2

If the interpreter used a different suffix for the bytecode file name, then the user can specify it by calling the `--suffix` or `-s` argument.

### Bytecode folder detection
The program is made as to expect the bytecode to always be inside a folder, as is costumary for Python for quite some time now. The default value for this folder is `__pycache__` but it can be specified by calling the `--cache` or the `-c` argument.

### Best way to use PyToPyc
1. Delete all the bytecode from your program.
2. Run your program with the command: `python -OO your_programs_main_file.py`.

This is essential because the interpreter will then create just the necessary bytecode for running the program. There can be situations in which there is more bytecode than necessary (from unused modules and such). Furthermore, by passing the `-OO` argument, docstrings and `assert` statements will not be put in the bytecode, saving space.
3. Run PyToPyc with the following command: `PyToPyc.py your_programs_directory new_directory`.
