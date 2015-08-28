ctypes 소개
===========

순서
----
* 들어가며
* Python C Extension
* 쉬운 ctypes 사용법
* 좀더 복잡한 ctypes 사용법
* ctypesgen
* 다른 대안들
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
_위 코드는 C의 수학 라이브러리 libm.so에 있는 cos() 함수를 C Extension을 통해 호출하는 예제로  [이곳](https://scipy-lectures.github.io/advanced/interfacing_with_c/interfacing_with_c.html)에서 잠시 빌려왔습니다._

* 무엇보다 이렇게 만든 코드는 Python __버전 의존성__을 갖게 되어 Python 인터프리터 버전이 바뀌면 동작하지 않습니다.


쉬운 ctypes 사용법
------------------
* ctypes는 ___C 언어의 타입(type)___을 쉽게 다룰 수 있도록 ___Python 2.5___ 버전부터 표준 라이브러리에 포함된 모듈입니다.
* C 언어로 Native 코드를 작성할 필요 없이 아래와 같이 동적 라이브러리를 바로 불러서 입출력 타입만 지정하고 사용할 수 있습니다.
```python
import ctypes
from ctypes.util import find_library

libm = ctypes.cdll.LoadLibrary(find_library('m'))    # libm.so 혹은 맥의 경우 libm.dylib을 찾아 로드합니다.
libm.cos.argtypes = [ctypes.c_double,]    # 매개변수의 타입을 리스트로 차례로 지정해 줍니다.
libm.cos.restype = ctypes.c_double        # 리턴 타입을 지정해 줍니다.

print 'cos(1)  =', libm.cos(1.0)
print 'cos(0)  =', libm.cos(0.0)
print 'cos(pi) =', libm.cos(3.14159265359)
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
        ('matches' if libapr.apr_fnmatch('*.txt', 'name.ext', 2) == APR_SUCCESS
                   else 'does not match')
```


좀더 복잡한 ctypes 사용법
-------------------------


ctypesgen
---------


다른 대안들
-----------

* SWIG
* cffi


참고 링크
---------

* [한국어 위키](https://ko.wikipedia.org/wiki/Ctypes)
* [ctypes 공식 문서](https://docs.python.org/2/library/ctypes.html)
* [ctypesgen git 저장소](https://github.com/davidjamesca/ctypesgen)
