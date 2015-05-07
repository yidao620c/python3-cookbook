==============================
15.5 从扩张模块中定义和导出C的API
==============================

----------
问题
----------
You have a C extension module that internally defines a variety of useful functions that
you would like to export as a public C API for use elsewhere. You would like to use these
functions inside other extension modules, but don’t know how to link them together,
and doing it with the C compiler/linker seems excessively complicated (or impossible).

|

----------
解决方案
----------
This recipe focuses on the code written to handle Point objects, which were presented
in Recipe 15.4. If you recall, that C code included some utility functions like this:

/* Destructor function for points */
static void del_Point(PyObject *obj) {

  free(PyCapsule_GetPointer(obj,"Point"));
}

/* Utility functions */
static Point *PyPoint_AsPoint(PyObject *obj) {
  return (Point *) PyCapsule_GetPointer(obj, "Point");
}

static PyObject *PyPoint_FromPoint(Point *p, int must_free) {
  return PyCapsule_New(p, "Point", must_free ? del_Point : NULL);
}

The  problem  now  addressed  is  how  to  export  the  PyPoint_AsPoint()  and  Py
Point_FromPoint() functions as an API that other extension modules could use and
link to (e.g., if you have other extensions that also want to use the wrapped  Point
objects).
To solve this problem, start by introducing a new header file for the “sample” extension
called pysample.h. Put the following code in it:

/* pysample.h */
#include "Python.h"
#include "sample.h"
#ifdef __cplusplus
extern "C" {
#endif

/* Public API Table */
typedef struct {
  Point *(*aspoint)(PyObject *);
  PyObject *(*frompoint)(Point *, int);
} _PointAPIMethods;

#ifndef PYSAMPLE_MODULE
/* Method table in external module */
static _PointAPIMethods *_point_api = 0;

/* Import the API table from sample */
static int import_sample(void) {
  _point_api = (_PointAPIMethods *) PyCapsule_Import("sample._point_api",0);
  return (_point_api != NULL) ? 1 : 0;
}

/* Macros to implement the programming interface */
#define PyPoint_AsPoint(obj) (_point_api->aspoint)(obj)
#define PyPoint_FromPoint(obj) (_point_api->frompoint)(obj)
#endif

#ifdef __cplusplus
}
#endif

The most important feature here is the _PointAPIMethods table of function pointers. It
will be initialized in the exporting module and found by importing modules.
Change the original extension module to populate the table and export it as follows:

/* pysample.c */

#include "Python.h"
#define PYSAMPLE_MODULE
#include "pysample.h"

...
/* Destructor function for points */
static void del_Point(PyObject *obj) {
  printf("Deleting point\n");
  free(PyCapsule_GetPointer(obj,"Point"));
}

/* Utility functions */
static Point *PyPoint_AsPoint(PyObject *obj) {
  return (Point *) PyCapsule_GetPointer(obj, "Point");
}

static PyObject *PyPoint_FromPoint(Point *p, int free) {
  return PyCapsule_New(p, "Point", free ? del_Point : NULL);
}

static _PointAPIMethods _point_api = {
  PyPoint_AsPoint,
  PyPoint_FromPoint
};
...

/* Module initialization function */
PyMODINIT_FUNC
PyInit_sample(void) {
  PyObject *m;
  PyObject *py_point_api;

  m = PyModule_Create(&samplemodule);
  if (m == NULL)
    return NULL;

  /* Add the Point C API functions */
  py_point_api = PyCapsule_New((void *) &_point_api, "sample._point_api", NULL);
  if (py_point_api) {
    PyModule_AddObject(m, "_point_api", py_point_api);
  }
  return m;
}

Finally, here is an example of a new extension module that loads and uses these API
functions:

/* ptexample.c */

/* Include the header associated with the other module */
#include "pysample.h"

/* An extension function that uses the exported API */
static PyObject *print_point(PyObject *self, PyObject *args) {
  PyObject *obj;
  Point *p;
  if (!PyArg_ParseTuple(args,"O", &obj)) {
    return NULL;
  }

  /* Note: This is defined in a different module */
  p = PyPoint_AsPoint(obj);
  if (!p) {
    return NULL;
  }
  printf("%f %f\n", p->x, p->y);
  return Py_BuildValue("");
}

static PyMethodDef PtExampleMethods[] = {
  {"print_point", print_point, METH_VARARGS, "output a point"},
  { NULL, NULL, 0, NULL}
};

static struct PyModuleDef ptexamplemodule = {
  PyModuleDef_HEAD_INIT,
  "ptexample",           /* name of module */
  "A module that imports an API",  /* Doc string (may be NULL) */
  -1,                 /* Size of per-interpreter state or -1 */
  PtExampleMethods       /* Method table */
};

/* Module initialization function */
PyMODINIT_FUNC
PyInit_ptexample(void) {
  PyObject *m;

  m = PyModule_Create(&ptexamplemodule);
  if (m == NULL)
    return NULL;

  /* Import sample, loading its API functions */
  if (!import_sample()) {
    return NULL;
  }

  return m;
}

When compiling this new module, you don’t even need to bother to link against any of
the libraries or code from the other module. For example, you can just make a simple
setup.py file like this:

# setup.py
from distutils.core import setup, Extension

setup(name='ptexample',
      ext_modules=[
        Extension('ptexample',
                  ['ptexample.c'],
                  include_dirs = [],  # May need pysample.h directory
                  )
        ]
)

If it all works, you’ll find that your new extension function works perfectly with the C
API functions defined in the other module:

>>> import sample
>>> p1 = sample.Point(2,3)
>>> p1
<capsule object "Point *" at 0x1004ea330>
>>> import ptexample
>>> ptexample.print_point(p1)
2.000000 3.000000
>>>

|

----------
讨论
----------
This recipe relies on the fact that capsule objects can hold a pointer to anything you
wish. In this case, the defining module populates a structure of function pointers, creates
a capsule that points to it, and saves the capsule in a module-level attribute (e.g., sam
ple._point_api).
Other modules can be programmed to pick up this attribute when imported and extract
the underlying pointer. In fact, Python provides the PyCapsule_Import() utility func‐
tion, which takes care of all the steps for you. You simply give it the name of the attribute
(e.g., sample._point_api), and it will find the capsule and extract the pointer all in one
step.
There are some C programming tricks involved in making exported functions look
normal in other modules. In the pysample.h file, a pointer _point_api is used to point
to the method table that was initialized in the exporting module. A related function
import_sample() is used to perform the required capsule import and initialize this
pointer. This function must be called before any functions are used. Normally, it would

be called in during module initialization. Finally, a set of C preprocessor macros have
been defined to transparently dispatch the API functions through the method table.
The user just uses the original function names, but doesn’t know about the extra indi‐
rection through these macros.
Finally, there is another important reason why you might use this technique to link
modules together—it’s actually easier and it keeps modules more cleanly decoupled. If
you didn’t want to use this recipe as shown, you might be able to cross-link modules
using advanced features of shared libraries and the dynamic loader. For example, putting
common API functions into a shared library and making sure that all extension modules
link against that shared library. Yes, this works, but it can be tremendously messy in
large systems. Essentially, this recipe cuts out all of that magic and allows modules to
link to one another through Python’s normal import mechanism and just a tiny number
of capsule calls. For compilation of modules, you only need to worry about header files,
not the hairy details of shared libraries.
Further information about providing C APIs for extension modules can be found in the
Python documentation.
