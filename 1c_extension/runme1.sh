#!/bin/sh

# build
python setup.py build_ext --inplace > /dev/null 2>&1

# examples
echo "==== example1 ===="
python example1.py

# clean
rm -rf build cos_module.so
