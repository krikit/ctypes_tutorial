ctypes 소개
===========

순서
----
* 들어가며
* Python C Extension
* 쉬운 ctypes 사용법
* 좀더 복잡한 ctypes 사용법
* ctypesgen
* 팁
* 참고 링크

들어가며
--------
* Python의 큰 매력 중의 하나는 바로 ___생산성___입니다.
* 수많은 ___라이브러리___들이 [Standard Library](https://docs.python.org/2/library/)로 제공되고, [Python Package Index](https://pypi.python.org/pypi)를 통해 더 많은 라이브러리들을 가져다 활용할 수 있습니다.
* 그리고 Python으로 포팅되지 않은 무수히 많은 ___C 라이브러리___들이 또한 존재합니다.
* 때로는 ___성능___을 이유로 C 언어를 사용하게 되기도 합니다. 많이들 사용하는 [NumPy](http://www.numpy.org/)도 성능을 위해 코어는 C 언어를 사용합니다.
* 이렇게 Python으로서는 외래어(?)인 C 언어로 만들어진 함수를 호출하거나 데이터를 주고 받는 것을 ___[Forein Function Interface](https://en.wikipedia.org/wiki/Foreign_function_interface)___라고 합니다.
* Python은 이러한 부분에 있어서도 매우 편리한 방법을 제공합니다.

Python C Extension
------------------
* Java에 JNI가 있다면 Python에는 ___[Python C Extension](https://docs.python.org/2/extending/extending.html)___이 있습니다.
* 그러나 아래와 같이 무시무시한(?) ___boilerplate 코드___들을 필요로하며 생소하고 어렵습니다.
```C
/*  Example of wrapping cos function from math.h with the Python-C-API. */

#include <Python.h>
#include <math.h>

/*  wrapped cosine function */
static PyObject* cos_func(PyObject* self, PyObject* args)
{
    double value;
    double answer;

    /*  parse the input, from python float to c double */
    if (!PyArg_ParseTuple(args, "d", &value))
        return NULL;
    /* if the above function returns -1, an appropriate Python exception will
     * have been set, and the function simply returns NULL
     */

    /* call cos from libm */
    answer = cos(value);

    /*  construct the output from cos, from c double to python float */
    return Py_BuildValue("f", answer);
}

/*  define functions in module */
static PyMethodDef CosMethods[] =
{
     {"cos_func", cos_func, METH_VARARGS, "evaluate the cosine"},
     {NULL, NULL, 0, NULL}
};

/* module initialization */
PyMODINIT_FUNC

initcos_module(void)
{
     (void) Py_InitModule("cos_module", CosMethods);
}
```
_위 코드는 C의 math 라이브러리 libm.so에 있는 cos() 함수를 C Extension을 통해 호출하는 예제로  [이곳](https://scipy-lectures.github.io/advanced/interfacing_with_c/interfacing_with_c.html)에서 잠시 빌려왔습니다._

* 무엇보다 이렇게 만든 코드는 Python ___버전 의존성___을 갖게 되어 Python 인터프리터 버전이 바뀌면 동작하지 않습니다.


쉬운 ctypes 사용법
------------------
* ctypes는 ___C 언어의 타입(type)___을 쉽게 다룰 수 있도록 ___Python 2.5___ 버전부터 표준 라이브러리에 포함된 모듈입니다.
* C 언어로 Native 코드를 작성할 필요 없이 아래와 같이 동적 라이브러리를 바로 불러서 입출력 타입만 지정하고 사용할 수 있습니다.
```python
import ctypes
from ctypes.util import find_library

libm = ctypes.cdll.LoadLibrary(find_library('m'))    # libm.so 혹은 맥의 경우 libm.dylib을 찾아 로드합니다.
libm.cos.argtypes = [ctypes.c_double,]               # 매개변수의 타입을 리스트로 차례로 지정해 줍니다.
libm.cos.restype = ctypes.c_double                   # 리턴 타입을 지정해 줍니다.

print 'cos(1)  =', libm.cos(1.0)              # 출력: 0.540302305868
print 'cos(0)  =', libm.cos(0.0)              # 출력: 1.0
print 'cos(pi) =', libm.cos(3.14159265359)    # 출력: -1.0
```

* [APR](http://apr.apache.org/) 라이브러리에서 [apr_fnmatch](http://apr.apache.org/docs/apr/1.5/group__apr__fnmatch.html#gabe9c7d7efe6afc203a01befbc45bad96) 함수를 사용해 보겠습니다. (물론 Python에는 [fnmatch](https://docs.python.org/2/library/fnmatch.html) 모듈이 있습니다.)
```python
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
```


좀더 복잡한 ctypes 사용법
-------------------------
* 아래와 같은 C API 헤더(mylib.h) 파일이 있고,
```C
#ifndef __MYLIB_H__
#define __MYLIB_H__

/* node data structure of linked list */
typedef struct _node_t {
    int value;
    struct _node_t* next;
} node_t;

void init_node(node_t* node);    /* initialize node */
node_t* make_list(int num);      /* make list has 'num' number of nodes */
void del_list(node_t* head);     /* delete entire nodes in list */

#endif    /* __MYLIB_H__ */
```
* 이를 구현한 소스 코드(mylib.c)와 빌드한 shared 라이브러리(libmylib.so)가 있다고 하면,
```C
#include <stdlib.h>
#include "mylib.h"

/* set value as 0 and next pointer as NULL */
void init_node(node_t* node) {
    if (node == NULL) return;
    node->value = 0;
    node->next = NULL;
}

/* make liked list of 'num' number of nodes and return its head node */
node_t* make_list(int num) {
    node_t* head = NULL;
    node_t* curr = NULL;
    int cnt = 0;

    if (num == 0) return NULL;

    head = (node_t*) malloc(sizeof(node_t));
    init_node(head);
    head->value = 1;

    curr = head;
    for (cnt = 1; cnt < num; ++cnt) {
        curr->next = (node_t*) malloc(sizeof(node_t));
        init_node(curr->next);
        curr->next->value = cnt + 1;
        curr = curr->next;
    }

    return head;
}

/* delete node itself and next pointer recursively */
void del_list(node_t* head) {
    if (head == NULL) return;
    if (head->next != NULL) del_list(head->next);
    free(head);
}
```
* 아래와 같이 Python 코드에서 ctypes를 이용하여 사용할 수 있습니다.
```python
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
node.value = 100                               # value 값을 100으로 지정해 줬으나,
mylib.init_node(ctypes.byref(node))
print 'initialized value: %d' % node.value     # 출력: initialized value: 0

head = mylib.make_list(5)
curr = head
while curr:
    print 'value: %d' % curr.contents.value    # 출력: value: 1, value: 2, ... , value: 5
    curr = curr.contents.next

mylib.del_list(head)                           # 생성한 리스트 전체 메모리를 해제
```
* 그러나 여전히 코드가 ___장황___하고, ___API 변경___에 대처하기가 용이하지 않습니다.

ctypesgen
---------
* ctypesgen을 이용하면 손쉽게 이러한 ctypes를 이용해 명세해 줘야할 API를 ___자동___으로 모듈로 생성하는 것이 가능합니다.
* ctypesgen은 [PyPI](https://pypi.python.org/pypi/ctypesgen)에 등록되어 있으므로 pip를 통해 설치하거나, [GitHub](https://github.com/davidjamesca/ctypesgen) 직접 내려받아 설치할 수 있습니다.
* 아래 명령은 ctypesgen을 설치한 후 `mylib`이라는 Python 모듈을 자동으로 생성하는 명령어입니다.
```
ctypesgen.py -I. -L. -lmylib -o mylib.py mylib.h
```
* -I, -L, -l 옵션은 gcc에서 사용하는 옵션과 동일하고, -o 옵션을 통해 출력할 파일의 이름을, 입력으로는 API 헤더를 지정해 주면 됩니다.
* 이렇게 하면 아래와 같이 간단히 모듈을 import하여 사용할 수 있습니다.
```python
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
```

팁
--
* ctypesgen으로 생성한 모듈에 정의되어 있는 `String` 클래스는 ctypes의 `create_string_buffer()` 함수로 생성한 배열을 인자로 넘길 경우 에러를 발생합니다.
* `String` 클래스 정의 부분에 `def from_param(cls, obj):` 메소드를 찾아 아래 코드를 마지막 `else` 문 위에 추가해 주면 됩니다.
```python
        # Convert from c_char array
        elif isinstance(obj, c_char * len(obj)):
            return obj
```
_기회가 되면 해당 부분에 대해 pull request를 보내도록 하겠습니다._

참고 링크
---------

* [한국어 위키](https://ko.wikipedia.org/wiki/Ctypes)
* [ctypes 공식 문서](https://docs.python.org/2/library/ctypes.html)
* [ctypesgen git 저장소](https://github.com/davidjamesca/ctypesgen)
