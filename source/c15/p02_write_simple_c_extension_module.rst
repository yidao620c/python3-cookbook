==============================
15.2 简单的C扩展模块
==============================

----------
问题
----------
You want to write a simple C extension module directly using Python’s extension API
and no other tools.

Solution
For simple C code, it is straightforward to make a handcrafted extension module. As a
preliminary step, you probably want to make sure your C code has a proper header file.
For example,

/* sample.h */

#include <math.h>

extern int gcd(int, int);
extern int in_mandel(double x0, double y0, int n);
extern int divide(int a, int b, int *remainder);
extern double avg(double *a, int n);

typedef struct Point {
    double x,y;
} Point;

extern double distance(Point *p1, Point *p2);

Typically, this header would correspond to a library that has been compiled separately.
With that assumption, here is a sample extension module that illustrates the basics of
writing extension functions:

#include "Python.h"
#include "sample.h"

/* int gcd(int, int) */
static PyObject *py_gcd(PyObject *self, PyObject *args) {
  int x, y, result;

  if (!PyArg_ParseTuple(args,"ii", &x, &y)) {
    return NULL;
  }
  result = gcd(x,y);
  return Py_BuildValue("i", result);
}

/* int in_mandel(double, double, int) */
static PyObject *py_in_mandel(PyObject *self, PyObject *args) {
  double x0, y0;
  int n;
  int result;

  if (!PyArg_ParseTuple(args, "ddi", &x0, &y0, &n)) {
    return NULL;
  }
  result = in_mandel(x0,y0,n);
  return Py_BuildValue("i", result);
}

/* int divide(int, int, int *) */
static PyObject *py_divide(PyObject *self, PyObject *args) {
  int a, b, quotient, remainder;
  if (!PyArg_ParseTuple(args, "ii", &a, &b)) {
    return NULL;
  }
  quotient = divide(a,b, &remainder);
  return Py_BuildValue("(ii)", quotient, remainder);
}

/* Module method table */
static PyMethodDef SampleMethods[] = {
  {"gcd",  py_gcd, METH_VARARGS, "Greatest common divisor"},
  {"in_mandel", py_in_mandel, METH_VARARGS, "Mandelbrot test"},
  {"divide", py_divide, METH_VARARGS, "Integer division"},
  { NULL, NULL, 0, NULL}
};

/* Module structure */
static struct PyModuleDef samplemodule = {
  PyModuleDef_HEAD_INIT,

  "sample",           /* name of module */
  "A sample module",  /* Doc string (may be NULL) */
  -1,                 /* Size of per-interpreter state or -1 */
  SampleMethods       /* Method table */
};

/* Module initialization function */
PyMODINIT_FUNC
PyInit_sample(void) {
  return PyModule_Create(&samplemodule);
}

For building the extension module, create a setup.py file that looks like this:

# setup.py
from distutils.core import setup, Extension

setup(name='sample',
      ext_modules=[
        Extension('sample',
                  ['pysample.c'],
                  include_dirs = ['/some/dir'],
                  define_macros = [('FOO','1')],
                  undef_macros = ['BAR'],
                  library_dirs = ['/usr/local/lib'],
                  libraries = ['sample']
                  )
        ]
)

Now, to build the resulting library, simply use python3 buildlib.py build_ext --
inplace. For example:

bash % python3 setup.py build_ext --inplace
running build_ext
building 'sample' extension
gcc -fno-strict-aliasing -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes
 -I/usr/local/include/python3.3m -c pysample.c
 -o build/temp.macosx-10.6-x86_64-3.3/pysample.o
gcc -bundle -undefined dynamic_lookup
build/temp.macosx-10.6-x86_64-3.3/pysample.o \
 -L/usr/local/lib -lsample -o sample.so
bash %

As shown, this creates a shared library called sample.so. When compiled, you should
be able to start importing it as a module:

>>> import sample
>>> sample.gcd(35, 42)
7
>>> sample.in_mandel(0, 0, 500)
1
>>> sample.in_mandel(2.0, 1.0, 500)

0
>>> sample.divide(42, 8)
(5, 2)
>>>

If you are attempting these steps on Windows, you may need to spend some time fiddling
with your environment and the build environment to get extension modules to build
correctly.  Binary  distributions  of  Python  are  typically  built  using  Microsoft  Visual
Studio. To get extensions to work, you may have to compile them using the same or
compatible tools. See the Python documentation.

Discussion
Before attempting any kind of handwritten extension, it is absolutely critical that you
consult Python’s documentation on “Extending and Embedding the Python Interpret‐
er”. Python’s C extension API is large, and repeating all of it here is simply not practical.
However, the most important parts can be easily discussed.
First, in extension modules, functions that you write are all typically written with a
common prototype such as this:

static PyObject *py_func(PyObject *self, PyObject *args) {
  ...
}

PyObject is the C data type that represents any Python object. At a very high level, an
extension function is a C function that receives a tuple of Python objects (in PyObject
*args) and returns a new Python object as a result. The self argument to the function
is unused for simple extension functions, but comes into play should you want to define
new classes or object types in C (e.g., if the extension function were a method of a class,
then self would hold the instance).
The PyArg_ParseTuple() function is used to convert values from Python to a C rep‐
resentation. As input, it takes a format string that indicates the required values, such as
“i” for integer and “d” for double, as well as the addresses of C variables in which to place
the converted results. PyArg_ParseTuple() performs a variety of checks on the number
and type of arguments. If there is any mismatch with the format string, an exception is
raised and NULL is returned. By checking for this and simply returning NULL, an ap‐
propriate exception will have been raised in the calling code.
The Py_BuildValue() function is used to create Python objects from C data types. It
also accepts a format code to indicate the desired type. In the extension functions, it is
used to return results back to Python. One feature of Py_BuildValue() is that it can
build more complicated kinds of objects, such as tuples and dictionaries. In the code
for py_divide(), an example showing the return of a tuple is shown. However, here are
a few more examples:

return Py_BuildValue("i", 34);      // Return an integer
return Py_BuildValue("d", 3.4);     // Return a double
return Py_BuildValue("s", "Hello"); // Null-terminated UTF-8 string
return Py_BuildValue("(ii)", 3, 4); // Tuple (3, 4)

Near the bottom of any extension module, you will find a function table such as the
SampleMethods table shown in this recipe. This table lists C functions, the names to use
in Python, as well as doc strings. All modules are required to specify such a table, as it
gets used in the initialization of the module.
The final function PyInit_sample() is the module initialization function that executes
when the module is first imported. The primary job of this function is to register the
module object with the interpreter.
As a final note, it must be stressed that there is considerably more to extending Python
with C functions than what is shown here (in fact, the C API contains well over 500
functions in it). You should view this recipe simply as a stepping stone for getting started.
To do more, start with the documentation on the PyArg_ParseTuple() and Py_Build
Value() functions, and expand from there.
