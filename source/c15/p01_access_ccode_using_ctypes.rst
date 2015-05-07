==============================
15.1 使用ctypes访问C代码
==============================

----------
问题
----------
You have a small number of C functions that have been compiled into a shared library
or DLL. You would like to call these functions purely from Python without having to
write additional C code or using a third-party extension tool.

|

----------
解决方案
----------
For small problems involving C code, it is often easy enough to use the ctypes module
that is part of Python’s standard library. In order to use ctypes, you must first make
sure the C code you want to access has been compiled into a shared library that is
compatible with the Python interpreter (e.g., same architecture, word size, compiler,
etc.). For the purposes of this recipe, assume that a shared library, libsample.so, has
been created and that it contains nothing more than the code shown in the chapter
introduction. Further assume that the libsample.so file has been placed in the same
directory as the sample.py file shown next.
To access the resulting library, you make a Python module that wraps around it, such
as the following:
# sample.py
import ctypes
import os

# Try to locate the .so file in the same directory as this file
_file = 'libsample.so'
_path = os.path.join(*(os.path.split(__file__)[:-1] + (_file,)))
_mod = ctypes.cdll.LoadLibrary(_path)

# int gcd(int, int)
gcd = _mod.gcd
gcd.argtypes = (ctypes.c_int, ctypes.c_int)
gcd.restype = ctypes.c_int

# int in_mandel(double, double, int)
in_mandel = _mod.in_mandel
in_mandel.argtypes = (ctypes.c_double, ctypes.c_double, ctypes.c_int)
in_mandel.restype = ctypes.c_int

# int divide(int, int, int *)
_divide = _mod.divide
_divide.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
_divide.restype = ctypes.c_int

def divide(x, y):
    rem = ctypes.c_int()
    quot = _divide(x, y, rem)

    return quot,rem.value

# void avg(double *, int n)
# Define a special type for the 'double *' argument
class DoubleArrayType:
    def from_param(self, param):
        typename = type(param).__name__
        if hasattr(self, 'from_' + typename):
            return getattr(self, 'from_' + typename)(param)
        elif isinstance(param, ctypes.Array):
            return param
        else:
            raise TypeError("Can't convert %s" % typename)

    # Cast from array.array objects
    def from_array(self, param):
        if param.typecode != 'd':
            raise TypeError('must be an array of doubles')
        ptr, _ = param.buffer_info()
        return ctypes.cast(ptr, ctypes.POINTER(ctypes.c_double))

    # Cast from lists/tuples
    def from_list(self, param):
        val = ((ctypes.c_double)*len(param))(*param)
        return val

    from_tuple = from_list

    # Cast from a numpy array
    def from_ndarray(self, param):
        return param.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

DoubleArray = DoubleArrayType()
_avg = _mod.avg
_avg.argtypes = (DoubleArray, ctypes.c_int)
_avg.restype = ctypes.c_double

def avg(values):
    return _avg(values, len(values))

# struct Point { }
class Point(ctypes.Structure):
    _fields_ = [('x', ctypes.c_double),
                ('y', ctypes.c_double)]

# double distance(Point *, Point *)
distance = _mod.distance
distance.argtypes = (ctypes.POINTER(Point), ctypes.POINTER(Point))
distance.restype = ctypes.c_double

If all goes well, you should be able to load the module and use the resulting C functions.
For example:

>>> import sample
>>> sample.gcd(35,42)
7
>>> sample.in_mandel(0,0,500)
1
>>> sample.in_mandel(2.0,1.0,500)
0
>>> sample.divide(42,8)
(5, 2)
>>> sample.avg([1,2,3])
2.0
>>> p1 = sample.Point(1,2)
>>> p2 = sample.Point(4,5)
>>> sample.distance(p1,p2)
4.242640687119285
>>>

|

----------
讨论
----------
There are several aspects of this recipe that warrant some discussion. The first issue
concerns the overall packaging of C and Python code together. If you are using ctypes
to access C code that you have compiled yourself, you will need to make sure that the
shared library gets placed in a location where the sample.py module can find it. One
possibility is to put the resulting .so file in the same directory as the supporting Python
code. This is what’s shown at the first part of this recipe—sample.py looks at the __file__
variable to see where it has been installed, and then constructs a path that points to a
libsample.so file in the same directory.
If the C library is going to be installed elsewhere, then you’ll have to adjust the path
accordingly. If the C library is installed as a standard library on your machine, you might
be able to use the ctypes.util.find_library() function. For example:

>>> from ctypes.util import find_library
>>> find_library('m')
'/usr/lib/libm.dylib'
>>> find_library('pthread')
'/usr/lib/libpthread.dylib'
>>> find_library('sample')
'/usr/local/lib/libsample.so'
>>>

Again, ctypes won’t work at all if it can’t locate the library with the C code. Thus, you’ll
need to spend a few minutes thinking about how you want to install things.
Once you know where the C library is located, you use ctypes.cdll.LoadLibrary()
to load it. The following statement in the solution does this where  _path is the full
pathname to the shared library:

_mod = ctypes.cdll.LoadLibrary(_path)

Once a library has been loaded, you need to write statements that extract specific sym‐
bols and put type signatures on them. This is what’s happening in code fragments such
as this:

# int in_mandel(double, double, int)
in_mandel = _mod.in_mandel
in_mandel.argtypes = (ctypes.c_double, ctypes.c_double, ctypes.c_int)
in_mandel.restype = ctypes.c_int

In this code, the .argtypes attribute is a tuple containing the input arguments to a
function, and .restype is the return type. ctypes defines a variety of type objects (e.g.,
c_double, c_int, c_short, c_float, etc.) that represent common C data types. Attach‐
ing the type signatures is critical if you want to make Python pass the right kinds of
arguments and convert data correctly (if you don’t do this, not only will the code not
work, but you might cause the entire interpreter process to crash).
A somewhat tricky part of using ctypes is that the original C code may use idioms that
don’t map cleanly to Python. The divide() function is a good example because it returns
a value through one of its arguments. Although that’s a common C technique, it’s often
not clear how it’s supposed to work in Python. For example, you can’t do anything
straightforward like this:

>>> divide = _mod.divide
>>> divide.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
>>> x = 0
>>> divide(10, 3, x)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ctypes.ArgumentError: argument 3: <class 'TypeError'>: expected LP_c_int
instance instead of int
>>>

Even if this did work, it would violate Python’s immutability of integers and probably
cause the entire interpreter to be sucked into a black hole. For arguments involving
pointers, you usually have to construct a compatible ctypes object and pass it in like
this:

>>> x = ctypes.c_int()
>>> divide(10, 3, x)
3
>>> x.value
1
>>>

Here an instance of a ctypes.c_int is created and passed in as the pointer object. Unlike
a normal Python integer, a c_int object can be mutated. The .value attribute can be
used to either retrieve or change the value as desired.

For cases where the C calling convention is “un-Pythonic,” it is common to write a small
wrapper function. In the solution, this code makes the divide() function return the
two results using a tuple instead:
# int divide(int, int, int *)
_divide = _mod.divide
_divide.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
_divide.restype = ctypes.c_int

def divide(x, y):
    rem = ctypes.c_int()
    quot = _divide(x,y,rem)
    return quot, rem.value

The avg() function presents a new kind of challenge. The underlying C code expects
to receive a pointer and a length representing an array. However, from the Python side,
we must consider the following questions: What is an array? Is it a list? A tuple? An
array from the array module? A numpy array? Is it all of these? In practice, a Python
“array” could take many different forms, and maybe you would like to support multiple
possibilities.
The DoubleArrayType class shows how to handle this situation. In this class, a single
method from_param() is defined. The role of this method is to take a single parameter
and narrow it down to a compatible ctypes object (a pointer to a ctypes.c_double, in
the example). Within from_param(), you are free to do anything that you wish. In the
solution, the typename of the parameter is extracted and used to dispatch to a more
specialized method. For example, if a list is passed, the typename is list and a method
from_list() is invoked.
For lists and tuples, the from_list() method performs a conversion to a ctypes array
object. This looks a little weird, but here is an interactive example of converting a list to
a ctypes array:

>>> nums = [1, 2, 3]
>>> a = (ctypes.c_double * len(nums))(*nums)
>>> a
<__main__.c_double_Array_3 object at 0x10069cd40>
>>> a[0]
1.0
>>> a[1]
2.0
>>> a[2]
3.0
>>>

For array objects, the from_array() method extracts the underlying memory pointer
and casts it to a ctypes pointer object. For example:

>>> import array
>>> a = array.array('d',[1,2,3])
>>> a
array('d', [1.0, 2.0, 3.0])
>>> ptr_ = a.buffer_info()
>>> ptr
4298687200
>>> ctypes.cast(ptr, ctypes.POINTER(ctypes.c_double))
<__main__.LP_c_double object at 0x10069cd40>
>>>

The from_ndarray() shows comparable conversion code for numpy arrays.
By defining the DoubleArrayType class and using it in the type signature of avg(), as
shown, the function can accept a variety of different array-like inputs:

>>> import sample
>>> sample.avg([1,2,3])
2.0
>>> sample.avg((1,2,3))
2.0
>>> import array
>>> sample.avg(array.array('d',[1,2,3]))
2.0
>>> import numpy
>>> sample.avg(numpy.array([1.0,2.0,3.0]))
2.0
>>>

The last part of this recipe shows how to work with a simple C structure. For structures,
you simply define a class that contains the appropriate fields and types like this:

class Point(ctypes.Structure):
    _fields_ = [('x', ctypes.c_double),
                ('y', ctypes.c_double)]

Once defined, you can use the class in type signatures as well as in code that needs to
instantiate and work with the structures. For example:

>>> p1 = sample.Point(1,2)
>>> p2 = sample.Point(4,5)
>>> p1.x
1.0
>>> p1.y
2.0
>>> sample.distance(p1,p2)
4.242640687119285
>>>

A few final comments: ctypes is a useful library to know about if all you’re doing is
accessing a few C functions from Python. However, if you’re trying to access a large
library, you might want to look at alternative approaches, such as Swig (described in
Recipe 15.9) or Cython (described in Recipe 15.10).

The main problem with a large library is that since ctypes isn’t entirely automatic, you’ll
have to spend a fair bit of time writing out all of the type signatures, as shown in the
example. Depending on the complexity of the library, you might also have to write a
large number of small wrapper functions and supporting classes. Also, unless you fully
understand all of the low-level details of the C interface, including memory management
and error handling, it is often quite easy to make Python catastrophically crash with a
segmentation fault, access violation, or some similar error.
As an alternative to ctypes, you might also look at CFFI. CFFI provides much of the
same functionality, but uses C syntax and supports more advanced kinds of C code. As
of this writing, CFFI is still a relatively new project, but its use has been growing rapidly.
There has even been some discussion of including it in the Python standard library in
some future release. Thus, it’s definitely something to keep an eye on.
