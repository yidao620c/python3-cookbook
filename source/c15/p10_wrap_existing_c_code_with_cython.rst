==============================
15.10 用Cython包装C代码
==============================

----------
问题
----------
你想使用Cython来创建一个Python扩展模块，用来包装某个已存在的C函数库。

|

----------
解决方案
----------
使用Cython构建一个扩展模块看上去很手写扩展有些类似，
因为你需要创建很多包装函数。不过，跟前面不同的是，你不需要在C语言中做这些——代码看上去更像是Python。

作为准备，假设本章介绍部分的示例代码已经被编译到某个叫 ``libsample`` 的C函数库中了。
首先创建一个名叫 ``csample.pxd`` 的文件，如下所示：

::

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

这个文件在Cython中的作用就跟C的头文件一样。
初始声明 ``cdef  extern  from  "sample.h"`` 指定了所学的C头文件。
接下来的声明都是来自于那个头文件。文件名是 ``csample.pxd`` ，而不是 ``sample.pxd`` ——这点很重要。

下一步，创建一个名为 ``sample.pyx`` 的问题。
该文件会定义包装器，用来桥接Python解释器到 ``csample.pxd`` 中声明的C代码。

::

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

该文件更多的细节部分会在讨论部分详细展开。
最后，为了构建扩展模块，像下面这样创建一个 ``setup.py`` 文件：

.. code-block:: python

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

要构建我们测试的目标模块，像下面这样做：

::

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

如果一切顺利的话，你应该有了一个扩展模块 ``sample.so`` ，可在下面例子中使用：

::

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

|

----------
讨论
----------
本节包含了很多前面所讲的高级特性，包括数组操作、包装隐形指针和释放GIL。
每一部分都会逐个被讲述到，但是我们最好能复习一下前面几小节。
在顶层，使用Cython是基于C之上。.pxd文件仅仅只包含C定义（类似.h文件），
.pyx文件包含了实现（类似.c文件）。``cimport`` 语句被Cython用来导入.pxd文件中的定义。
它跟使用普通的加载Python模块的导入语句是不同的。

尽管 `.pxd` 文件包含了定义，但它们并不是用来自动创建扩展代码的。
因此，你还是要写包装函数。例如，就算 ``csample.pxd`` 文件声明了 ``int gcd(int, int)`` 函数，
你仍然需要在 ``sample.pyx`` 中为它写一个包装函数。例如：

.. code-block:: python

    cimport csample

    def gcd(unsigned int x, unsigned int y):
        return csample.gcd(x,y)

对于简单的函数，你并不需要去做太多的时。
Cython会生成包装代码来正确的转换参数和返回值。
绑定到属性上的C数据类型是可选的。不过，如果你包含了它们，你可以另外做一些错误检查。
例如，如果有人使用负数来调用这个函数，会抛出一个异常：

::

    >>> sample.gcd(-10,2)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "sample.pyx", line 7, in sample.gcd (sample.c:1284)
        def gcd(unsigned int x,unsigned int y):
    OverflowError: can't convert negative value to unsigned int
    >>>

如果你想对包装函数做另外的检查，只需要使用另外的包装代码。例如：

::

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
``in_mandel()`` 的声明

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
