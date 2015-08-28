import ctypes
from ctypes.util import find_library

APR_SUCCESS = 0

libapr = ctypes.cdll.LoadLibrary(find_library('apr-1'))
libapr.apr_fnmatch.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
libapr.apr_fnmatch.restype = ctypes.c_int

print '"*.ext" %s "name.ext"' % \
        ('matches' if libapr.apr_fnmatch('*.ext', 'name.ext', 0) == APR_SUCCESS
                   else 'does not match')
print '"*.txt" %s "name.ext"' % \
        ('matches' if libapr.apr_fnmatch('*.txt', 'name.ext', 0) == APR_SUCCESS
                   else 'does not match')
