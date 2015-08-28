import ctypes
import mylib

node = mylib.node_t()
node.value = 100
mylib.init_node(ctypes.byref(node))
print 'initialized value: %d' % node.value

head = mylib.make_list(5)
curr = head
while curr:
    print 'value: %d' % curr.contents.value
    curr = curr.contents.next

mylib.del_list(head)
