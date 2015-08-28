import ctypes
from ctypes.util import find_library

mylib = ctypes.cdll.LoadLibrary(find_library('mylib'))
