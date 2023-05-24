from os.path import isdir, exists, join, basename
from os import mkdir, listdir, rename
from compileall import compile_dir
from shutil import move
import shutil
from sys import argv


def rename_bytecode(outdir):  # Retira o sufixo dos arquivos pyc
    directories = []
    for i in listdir(outdir):
        directory = join(outdir, i)
        if not isdir(directory) and directory[-3:] == 'pyc':
            directories.append(directory)

    for file in directories:
        rename(file, file.replace(suffix, ''))


def move_misc(indir, outdir):  # Move outros arquivos miscelâneos.
    if not exists(outdir):
        mkdir(outdir)

    directories = []
    for i in listdir(indir):
        directory = join(indir, i)
        if not isdir(directory) and directory[-3:] != '.py' and directory[-3:] != 'pyc':
            directories.append(directory)

    for file in directories:
        move(file, outdir)

    rename_bytecode(outdir)


def move_bytecode(indir, outdir):  # Olha se esso diretório absolute tem uma pasta __pycache__ e move tudo para o diretório de saída
    if not exists(outdir):
        mkdir(outdir)

    if exists((join(indir, '__pycache__'))):
        for file in listdir(join(indir, '__pycache__')):
            try:
                move(join(indir, '__pycache__', file), outdir)
            except shutil.Error:
                pass


def recurse(dir):  # Vai entrando de pasta em pasta até não ter mais nada.
    move_bytecode(dir, join(output_dir, basename(dir)))
    move_misc(dir, join(output_dir, basename(dir)))

    directories = []
    for i in listdir(dir):  # Lê os diretórios donde está
        directory = join(dir, i)
        if isdir(directory) and '__pycache__' not in directory:
            directories.append(directory)

    if any(isdir(subdir) for subdir in directories):
        for subdir in directories:
            recurse(subdir)


if __name__ == '__main__':
    try:
        input_dir = argv[1]

        if input_dir[-1] != '/':
            input_dir += '/'

        if not exists(input_dir):
            raise 'Diretório de entrada não existe.'
    except IndexError:
        input_dir = ''

    try:
        output_dir = argv[2]

        if output_dir[-1] != '/':
            output_dir += '/'
    except IndexError:
        output_dir = '/'

    try:
        output_dir = argv[3]
    except IndexError:
        suffix = '.cpython-311'

    try:
        mkdir(output_dir)  # Cria o diretório de saída
    except FileExistsError:
        pass

    compile_dir(input_dir)  # Compila tudo
    # recurse(input_dir)
