#!/bin/sh

# build
python setup.py build_ext --inplace

# examples
echo "==== example1 ===="
python example1.py
