#!/bin/sh

# build
gcc -fPIC -shared -o libmylib.so mylib.c

# examples
echo "==== example4 ===="
python example4.py

# clean
rm -f libmylib.so
