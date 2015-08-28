#!/bin/sh

# check ctypesgen
which ctypesgen.py > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "You must install ctypesgen package with command like 'pip install ctypesgen'."
    echo "Or you can build with source from 'https://github.com/davidjamesca/ctypesgen'."
    exit 1
fi

# build
ln -sf ../3complicated_ctypes/mylib.h
ln -sf ../3complicated_ctypes/mylib.c
gcc -fPIC -shared -o libmylib.so mylib.c
ctypesgen.py -I. -L. -lmylib -o mylib.py mylib.h > /dev/null 2>&1

# examples
echo "==== example5 ===="
python example5.py

# clean
unlink mylib.h
unlink mylib.c
rm -f libmylib.so mylib.py mylib.pyc
