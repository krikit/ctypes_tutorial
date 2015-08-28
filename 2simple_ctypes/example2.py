import ctypes
from ctypes.util import find_library

libm = ctypes.cdll.LoadLibrary(find_library('m'))
libm.cos.argtypes = [ctypes.c_double,]
libm.cos.restype = ctypes.c_double

print 'cos(1)  =', libm.cos(1.0)
print 'cos(0)  =', libm.cos(0.0)
print 'cos(pi) =', libm.cos(3.14159265359)
