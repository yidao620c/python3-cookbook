==============================
15.11 用Cython写高性能的数组操作
==============================

----------
问题
----------
You would like to write some high-performance array processing functions to operate
on arrays from libraries such as NumPy. You’ve heard that tools such as Cython can
make this easier, but aren’t sure how to do it.

Solution
As an example, consider the following code which shows a Cython function for clipping
the values in a simple one-dimensional array of doubles:

# sample.pyx (Cython)

cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef clip(double[:] a, double min, double max, double[:] out):
    '''
    Clip the values in a to be between min and max. Result in out
    '''
    if min > max:
        raise ValueError("min must be <= max")
    if a.shape[0] != out.shape[0]:
        raise ValueError("input and output arrays must be the same size")
    for i in range(a.shape[0]):
        if a[i] < min:
            out[i] = min
        elif a[i] > max:
            out[i] = max
        else:
            out[i] = a[i]

To compile and build the extension, you’ll need a setup.py file such as the following (use
python3 setup.py build_ext --inplace to build it):

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension('sample',
              ['sample.pyx'])
]

setup(
  name = 'Sample app',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)

You will find that the resulting function clips arrays, and that it works with many dif‐
ferent kinds of array objects. For example:

>>> # array module example
>>> import sample
>>> import array
>>> a = array.array('d',[1,-3,4,7,2,0])
>>> a

array('d', [1.0, -3.0, 4.0, 7.0, 2.0, 0.0])
>>> sample.clip(a,1,4,a)
>>> a
array('d', [1.0, 1.0, 4.0, 4.0, 2.0, 1.0])

>>> # numpy example
>>> import numpy
>>> b = numpy.random.uniform(-10,10,size=1000000)
>>> b
array([-9.55546017,  7.45599334,  0.69248932, ...,  0.69583148,
       -3.86290931,  2.37266888])
>>> c = numpy.zeros_like(b)
>>> c
array([ 0.,  0.,  0., ...,  0.,  0.,  0.])
>>> sample.clip(b,-5,5,c)
>>> c
array([-5.        ,  5.        ,  0.69248932, ...,  0.69583148,
       -3.86290931,  2.37266888])
>>> min(c)
-5.0
>>> max(c)
5.0
>>>

You will also find that the resulting code is fast. The following session puts our imple‐
mentation in a head-to-head battle with the clip() function already present in numpy:

>>> timeit('numpy.clip(b,-5,5,c)','from __main__ import b,c,numpy',number=1000)
8.093049556000551
>>> timeit('sample.clip(b,-5,5,c)','from __main__ import b,c,sample',
...         number=1000)
3.760528204000366
>>>

As you can see, it’s quite a bit faster—an interesting result considering the core of the
NumPy version is written in C.

Discussion
This recipe utilizes Cython typed memoryviews, which greatly simplify code that op‐
erates on arrays. The declaration cpdef clip() declares clip() as both a C-level and
Python-level function. In Cython, this is useful, because it means that the function call
is more efficently called by other Cython functions (e.g., if you want to invoke clip()
from a different Cython function).
The typed parameters double[:] a and double[:] out declare those parameters as
one-dimensional  arrays  of  doubles.  As  input,  they  will  access  any  array  object  that
properly implements the memoryview interface, as described in PEP 3118. This includes
arrays from NumPy and from the built-in array library.

When writing code that produces a result that is also an array, you should follow the
convention shown of having an output parameter as shown. This places the responsi‐
bility of creating the output array on the caller and frees the code from having to know
too much about the specific details of what kinds of arrays are being manipulated (it
just assumes the arrays are already in-place and only needs to perform a few basic sanity
checks such as making sure their sizes are compatible). In libraries such as NumPy, it
is relatively easy to create output arrays using functions such as  numpy.zeros() or
numpy.zeros_like().  Alternatively,  to  create  uninitialized  arrays,  you  can  use  num
py.empty() or numpy.empty_like(). This will be slightly faster if you’re about to over‐
write the array contents with a result.
In the implementation of your function, you simply write straightforward looking array
processing code using indexing and array lookups (e.g., a[i], out[i], and so forth).
Cython will take steps to make sure these produce efficient code.
The two decorators that precede the definition of clip() are a few optional performance
optimizations. @cython.boundscheck(False) eliminates all array bounds checking and
can  be  used  if  you  know  the  indexing  won’t  go  out  of  range.  @cython.wrap
around(False) eliminates the handling of negative array indices as wrapping around
to the end of the array (like with Python lists). The inclusion of these decorators can
make the code run substantially faster (almost 2.5 times faster on this example when
tested).
Whenever working with arrays, careful study and experimentation with the underlying
algorithm can also yield large speedups. For example, consider this variant of the clip()
function that uses conditional expressions:

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef clip(double[:] a, double min, double max, double[:] out):
    if min > max:
        raise ValueError("min must be <= max")
    if a.shape[0] != out.shape[0]:
        raise ValueError("input and output arrays must be the same size")
    for i in range(a.shape[0]):
        out[i] = (a[i] if a[i] < max else max) if a[i] > min else min

When tested, this version of the code runs over 50% faster (2.44s versus 3.76s on the
timeit() test shown earlier).
At this point, you might be wondering how this code would stack up against a hand‐
written C version. For example, perhaps you write the following C function and craft a
handwritten extension to using techniques shown in earlier recipes:

void clip(double *a, int n, double min, double max, double *out) {
  double x;
  for (; n >= 0; n--, a++, out++) {
    x = *a;

    *out = x > max ? max : (x < min ? min : x);
  }
}

The extension code for this isn’t shown, but after experimenting, we found that a hand‐
crafted C extension ran more than 10% slower than the version created by Cython. The
bottom line is that the code runs a lot faster than you might think.
There are several extensions that can be made to the solution code. For certain kinds of
array operations, it might make sense to release the GIL so that multiple threads can
run in parallel. To do that, modify the code to include the with nogil: statement:

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef clip(double[:] a, double min, double max, double[:] out):
    if min > max:
        raise ValueError("min must be <= max")
    if a.shape[0] != out.shape[0]:
        raise ValueError("input and output arrays must be the same size")
    with nogil:
        for i in range(a.shape[0]):
            out[i] = (a[i] if a[i] < max else max) if a[i] > min else min

If you want to write a version of the code that operates on two-dimensional arrays, here
is what it might look like:

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef clip2d(double[:,:] a, double min, double max, double[:,:] out):
    if min > max:
        raise ValueError("min must be <= max")
    for n in range(a.ndim):
        if a.shape[n] != out.shape[n]:
            raise TypeError("a and out have different shapes")
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            if a[i,j] < min:
                out[i,j] = min
            elif a[i,j] > max:
                out[i,j] = max
            else:
                out[i,j] = a[i,j]

Hopefully it’s not lost on the reader that all of the code in this recipe is not tied to any
specific array library (e.g., NumPy). That gives the code a great deal of flexibility. How‐
ever, it’s also worth noting that dealing with arrays can be significantly more complicated
once multiple dimensions, strides, offsets, and other factors are introduced. Those top‐
ics are beyond the scope of this recipe, but more information can be found in PEP
3118. The Cython documentation on “typed memoryviews” is also essential reading.

