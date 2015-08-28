#!/bin/sh

# build
gcc -shared -o libmylib.so mylib.c

# examples
echo "==== example4 ===="
python example4.py
