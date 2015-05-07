==============================
15.10 用Cython包装C代码
==============================

----------
问题
----------
You want to use Cython to make a Python extension module that wraps around an
existing C library.

Solution
Making an extension module with Cython looks somewhat similar to writing a hand‐
written extension, in that you will be creating a collection of wrapper functions. How‐
ever, unlike previous recipes, you won’t be doing this in C—the code will look a lot more
like Python.
As preliminaries, assume that the sample code shown in the introduction to this chapter
has been compiled into a C library called  libsample. Start by creating a file named
csample.pxd that looks like this:

# csample.pxd
#
# Declarations of "external" C functions and structures

cdef extern from "sample.h":
    int gcd(int, int)
    bint in_mandel(double, double, int)
    int divide(int, int, int *)
    double avg(double *, int) nogil

    ctypedef struct Point:
         double x
         double y

    double distance(Point *, Point *)

This file serves the same purpose in Cython as a C header file. The initial declaration
cdef  extern  from  "sample.h"  declares  the  required  C  header  file.  Declarations
that follow are taken from that header. The name of this file is csample.pxd, not sam‐
ple.pxd—this is important.
Next, create a file named sample.pyx. This file will define wrappers that bridge the
Python interpreter to the underlying C code declared in the csample.pxd file:

# sample.pyx

# Import the low-level C declarations
cimport csample

# Import some functionality from Python and the C stdlib
from cpython.pycapsule cimport *

from libc.stdlib cimport malloc, free

# Wrappers
def gcd(unsigned int x, unsigned int y):
    return csample.gcd(x, y)

def in_mandel(x, y, unsigned int n):
    return csample.in_mandel(x, y, n)

def divide(x, y):
    cdef int rem
    quot = csample.divide(x, y, &rem)
    return quot, rem

def avg(double[:] a):
    cdef:
        int sz
        double result

    sz = a.size
    with nogil:
        result = csample.avg(<double *> &a[0], sz)
    return result

# Destructor for cleaning up Point objects
cdef del_Point(object obj):
    pt = <csample.Point *> PyCapsule_GetPointer(obj,"Point")
    free(<void *> pt)

# Create a Point object and return as a capsule
def Point(double x,double y):
    cdef csample.Point *p
    p = <csample.Point *> malloc(sizeof(csample.Point))
    if p == NULL:
        raise MemoryError("No memory to make a Point")
    p.x = x
    p.y = y
    return PyCapsule_New(<void *>p,"Point",<PyCapsule_Destructor>del_Point)

def distance(p1, p2):
    pt1 = <csample.Point *> PyCapsule_GetPointer(p1,"Point")
    pt2 = <csample.Point *> PyCapsule_GetPointer(p2,"Point")
    return csample.distance(pt1,pt2)

Various details of this file will be covered further in the discussion section. Finally, to
build the extension module, create a setup.py file that looks like this:

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension('sample',

              ['sample.pyx'],
              libraries=['sample'],
              library_dirs=['.'])]
setup(
  name = 'Sample extension module',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)

To build the resulting module for experimentation, type this:

bash % python3 setup.py build_ext --inplace
running build_ext
cythoning sample.pyx to sample.c
building 'sample' extension
gcc -fno-strict-aliasing -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes
 -I/usr/local/include/python3.3m -c sample.c
 -o build/temp.macosx-10.6-x86_64-3.3/sample.o
gcc -bundle -undefined dynamic_lookup build/temp.macosx-10.6-x86_64-3.3/sample.o
  -L. -lsample -o sample.so
bash %

If it works, you should have an extension module sample.so that can be used as shown
in the following example:

>>> import sample
>>> sample.gcd(42,10)
2
>>> sample.in_mandel(1,1,400)
False
>>> sample.in_mandel(0,0,400)
True
>>> sample.divide(42,10)
(4, 2)
>>> import array
>>> a = array.array('d',[1,2,3])
>>> sample.avg(a)
2.0
>>> p1 = sample.Point(2,3)
>>> p2 = sample.Point(4,5)
>>> p1
<capsule object "Point" at 0x1005d1e70>
>>> p2
<capsule object "Point" at 0x1005d1ea0>
>>> sample.distance(p1,p2)
2.8284271247461903
>>>

Discussion
This recipe incorporates a number of advanced features discussed in prior recipes, in‐
cluding manipulation of arrays, wrapping opaque pointers, and releasing the GIL. Each
of these parts will be discussed in turn, but it may help to review earlier recipes first.
At a high level, using Cython is modeled after C. The .pxd files merely contain C defi‐
nitions (similar to .h files) and the .pyx files contain implementation (similar to a .c file).
The cimport statement is used by Cython to import definitions from a .pxd file. This is
different than using a normal Python import statement, which would load a regular
Python module.
Although .pxd files contain definitions, they are not used for the purpose of automati‐
cally creating extension code. Thus, you still have to write simple wrapper functions.
For example, even though the csample.pxd file declares int gcd(int, int) as a func‐
tion, you still have to write a small wrapper for it in sample.pyx. For instance:

cimport csample

def gcd(unsigned int x, unsigned int y):
    return csample.gcd(x,y)

For simple functions, you don’t have to do too much. Cython will generate wrapper code
that properly converts the arguments and return value. The C data types attached to the
arguments are optional. However, if you include them, you get additional error checking
for free. For example, if someone calls this function with negative values, an exception
is generated:

>>> sample.gcd(-10,2)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "sample.pyx", line 7, in sample.gcd (sample.c:1284)
    def gcd(unsigned int x,unsigned int y):
OverflowError: can't convert negative value to unsigned int
>>>

If you want to add additional checking to the wrapper, just use additional wrapper code.
For example:

def gcd(unsigned int x, unsigned int y):
    if x <= 0:
        raise ValueError("x must be > 0")
    if y <= 0:
        raise ValueError("y must be > 0")
    return csample.gcd(x,y)

The declaration of in_mandel() in the csample.pxd file has an interesting, but subtle
definition. In that file, the function is declared as returning a bint instead of an int.
This causes the function to create a proper Boolean value from the result instead of a
simple integer. So, a return value of 0 gets mapped to False and 1 to True.

Within the Cython wrappers, you have the option of declaring C data types in addition
to using all of the usual Python objects. The wrapper for divide() shows an example
of this as well as how to handle a pointer argument.

def divide(x,y):
    cdef int rem
    quot = csample.divide(x,y,&rem)
    return quot, rem

Here, the rem variable is explicitly declared as a C int variable. When passed to the
underlying divide() function, &rem makes a pointer to it just as in C.
The code for the avg() function illustrates some more advanced features of Cython.
First the declaration def avg(double[:] a) declares avg() as taking a one-dimensional
memoryview of double values. The amazing part about this is that the resulting function
will accept any compatible array object, including those created by libraries such as
numpy. For example:
>>> import array
>>> a = array.array('d',[1,2,3])
>>> import numpy
>>> b = numpy.array([1., 2., 3.])
>>> import sample
>>> sample.avg(a)
2.0
>>> sample.avg(b)
2.0
>>>

In the wrapper, a.size and &a[0] refer to the number of array items and underlying
pointer, respectively. The syntax <double *> &a[0] is how you type cast pointers to a
different type if necessary. This is needed to make sure the C avg() receives a pointer
of the correct type. Refer to the next recipe for some more advanced usage of Cython
memoryviews.
In addition to working with general arrays, the avg() example also shows how to work
with the global interpreter lock. The statement with nogil: declares a block of code as
executing without the GIL. Inside this block, it is illegal to work with any kind of normal
Python object—only objects and functions declared as cdef can be used. In addition to
that, external functions must explicitly declare that they can execute without the GIL.
Thus, in the csample.pxd file, the avg() is declared as double avg(double *, int)
nogil.
The handling of the Point structure presents a special challenge. As shown, this recipe
treats  Point  objects  as  opaque  pointers  using  capsule  objects,  as  described  in
Recipe 15.4. However, to do this, the underlying Cython code is a bit more complicated.
First, the following imports are being used to bring in definitions of functions from the
C library and Python C API:

from cpython.pycapsule cimport *
from libc.stdlib cimport malloc, free

The function del_Point() and Point() use this functionality to create a capsule object
that  wraps  around  a  Point  *  pointer.  The  declaration  cdef  del_Point()  declares
del_Point() as a function that is only accessible from Cython and not Python. Thus,
this function will not be visible to the outside—instead, it’s used as a callback function
to  clean  up  memory  allocated  by  the  capsule.  Calls  to  functions  such  as  PyCap
sule_New(), PyCapsule_GetPointer() are directly from the Python C API and are used
in the same way.
The distance() function has been written to extract pointers from the capsule objects
created by Point(). One notable thing here is that you simply don’t have to worry about
exception handling. If a bad object is passed, PyCapsule_GetPointer() raises an ex‐
ception,  but  Cython  already  knows  to  look  for  it  and  propagate  it  out  of  the  dis
tance() function if it occurs.
A downside to the handling of Point structures is that they will be completely opaque
in this implementation. You won’t be able to peek inside or access any of their attributes.
There is an alternative approach to wrapping, which is to define an extension type, as
shown in this code:

# sample.pyx

cimport csample
from libc.stdlib cimport malloc, free
...

cdef class Point:
    cdef csample.Point *_c_point
    def __cinit__(self, double x, double y):
        self._c_point = <csample.Point *> malloc(sizeof(csample.Point))
        self._c_point.x = x
        self._c_point.y = y

    def __dealloc__(self):
        free(self._c_point)

    property x:
        def __get__(self):
            return self._c_point.x
        def __set__(self, value):
            self._c_point.x = value

    property y:
        def __get__(self):
            return self._c_point.y
        def __set__(self, value):
            self._c_point.y = value

def distance(Point p1, Point p2):
    return csample.distance(p1._c_point, p2._c_point)

Here, the cdef class Point is declaring Point as an extension type. The class variable
cdef csample.Point *_c_point is declaring an instance variable that holds a pointer
to an underlying Point structure in C. The __cinit__() and __dealloc__() methods
create and destroy the underlying C structure using malloc() and free() calls. The
property x and property y declarations give code that gets and sets the underlying
structure attributes. The wrapper for distance() has also been suitably modified to
accept instances of the  Point extension type as arguments, but pass the underlying
pointer to the C function.
Making this change, you will find that the code for manipulating Point objects is more
natural:

>>> import sample
>>> p1 = sample.Point(2,3)
>>> p2 = sample.Point(4,5)
>>> p1
<sample.Point object at 0x100447288>
>>> p2
<sample.Point object at 0x1004472a0>
>>> p1.x
2.0
>>> p1.y
3.0
>>> sample.distance(p1,p2)
2.8284271247461903
>>>

This recipe has illustrated many of Cython’s core features that you might be able to
extrapolate to more complicated kinds of wrapping. However, you will definitely want
to read more of the official documentation to do more.
The next few recipes also illustrate a few additional Cython features.
