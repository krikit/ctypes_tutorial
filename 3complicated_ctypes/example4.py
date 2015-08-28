import ctypes
from ctypes import Structure, POINTER

class node_t(Structure):
    pass

node_t._fields_ = [
        ('value', ctypes.c_int),
        ('next', POINTER(node_t))
]

mylib = ctypes.cdll.LoadLibrary('./libmylib.so')
mylib.init_node.argtypes = [POINTER(node_t),]
mylib.make_list.restype = POINTER(node_t)
mylib.del_list.argtypes = [POINTER(node_t),]

node = node_t()
node.value = 100
mylib.init_node(ctypes.byref(node))
print 'initialized value: %d' % node.value

head = mylib.make_list(5)
curr = head
while curr:
    print 'value: %d' % curr.contents.value
    curr = curr.contents.next

mylib.del_list(head)
