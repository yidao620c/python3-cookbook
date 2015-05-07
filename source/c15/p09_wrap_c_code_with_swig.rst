==============================
15.9 用WSIG包装C代码
==============================

----------
问题
----------
You have existing C code that you would like to access as a C extension module. You
would like to do this using the Swig wrapper generator.

Solution
Swig operates by parsing C header files and automatically creating extension code. To
use it, you first need to have a C header file. For example, this header file for our sample
code:

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

Once you have the header files, the next step is to write a Swig “interface” file. By con‐
vention, these files have a .i suffix and might look similar to the following:

// sample.i - Swig interface
%module sample
%{
#include "sample.h"
%}

/* Customizations */
%extend Point {
    /* Constructor for Point objects */
    Point(double x, double y) {
        Point *p = (Point *) malloc(sizeof(Point));
        p->x = x;
        p->y = y;
        return p;
   };
};

/* Map int *remainder as an output argument */
%include typemaps.i
%apply int *OUTPUT { int * remainder };

/* Map the argument pattern (double *a, int n) to arrays */
%typemap(in) (double *a, int n)(Py_buffer view) {
  view.obj = NULL;
  if (PyObject_GetBuffer($input, &view, PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT) == -1) {
    SWIG_fail;
  }
  if (strcmp(view.format,"d") != 0) {
    PyErr_SetString(PyExc_TypeError, "Expected an array of doubles");
    SWIG_fail;
  }
  $1 = (double *) view.buf;
  $2 = view.len / sizeof(double);
}

%typemap(freearg) (double *a, int n) {
  if (view$argnum.obj) {
    PyBuffer_Release(&view$argnum);
  }
}

/* C declarations to be included in the extension module */

extern int gcd(int, int);
extern int in_mandel(double x0, double y0, int n);
extern int divide(int a, int b, int *remainder);
extern double avg(double *a, int n);

typedef struct Point {
    double x,y;
} Point;

extern double distance(Point *p1, Point *p2);

Once you have written the interface file, Swig is invoked as a command-line tool:

bash % swig -python -py3 sample.i
bash %

The output of swig is two files, sample_wrap.c and sample.py. The latter file is what
users import. The sample_wrap.c file is C code that needs to be compiled into a sup‐
porting module called _sample. This is done using the same techniques as for normal
extension modules. For example, you create a setup.py file like this:

# setup.py
from distutils.core import setup, Extension

setup(name='sample',
      py_modules=['sample.py'],
      ext_modules=[
        Extension('_sample',
                  ['sample_wrap.c'],
                  include_dirs = [],
                  define_macros = [],

                  undef_macros = [],
                  library_dirs = [],
                  libraries = ['sample']
                  )
        ]
)

To compile and test, run python3 on the setup.py file like this:

bash % python3 setup.py build_ext --inplace
running build_ext
building '_sample' extension
gcc -fno-strict-aliasing -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes
-I/usr/local/include/python3.3m -c sample_wrap.c
 -o build/temp.macosx-10.6-x86_64-3.3/sample_wrap.o
sample_wrap.c: In function ‘SWIG_InitializeModule’:
sample_wrap.c:3589: warning: statement with no effect
gcc -bundle -undefined dynamic_lookup build/temp.macosx-10.6-x86_64-3.3/sample.o
 build/temp.macosx-10.6-x86_64-3.3/sample_wrap.o -o _sample.so -lsample
bash %

If all of this works, you’ll find that you can use the resulting C extension module in a
straightforward way. For example:

>>> import sample
>>> sample.gcd(42,8)
2
>>> sample.divide(42,8)
[5, 2]
>>> p1 = sample.Point(2,3)
>>> p2 = sample.Point(4,5)
>>> sample.distance(p1,p2)
2.8284271247461903
>>> p1.x
2.0
>>> p1.y
3.0
>>> import array
>>> a = array.array('d',[1,2,3])
>>> sample.avg(a)
2.0
>>>

Discussion
Swig is one of the oldest tools for building extension modules, dating back to Python
Python. Swig can automate much of the wrapper generation process.

All Swig interfaces tend to start with a short preamble like this:

%module sample
%{
#include "sample.h"
%}

This merely declares the name of the extension module and specifies C header files that
must be included to make everything compile (the code enclosed in %{ and %} is pasted
directly into the output code so this is where you put all included files and other defi‐
nitions needed for compilation).
The bottom part of a Swig interface is a listing of C declarations that you want to be
included in the extension. This is often just copied from the header files. In our example,
we just pasted in the header file directly like this:

%module sample
%{
#include "sample.h"
%}
...
extern int gcd(int, int);
extern int in_mandel(double x0, double y0, int n);
extern int divide(int a, int b, int *remainder);
extern double avg(double *a, int n);

typedef struct Point {
    double x,y;
} Point;

extern double distance(Point *p1, Point *p2);

It is important to stress that these declarations are telling Swig what you want to include
in the Python module. It is quite common to edit the list of declarations or to make
modifications as appropriate. For example, if you didn’t want certain declarations to be
included, you would remove them from the declaration list.
The most complicated part of using Swig is the various customizations that it can apply
to the C code. This is a huge topic that can’t be covered in great detail here, but a number
of such customizations are shown in this recipe.
The first customization involving the %extend directive allows methods to be attached
to existing structure and class definitions. In the example, this is used to add a con‐
structor method to the Point structure. This customization makes it possible to use the
structure like this:

>>> p1 = sample.Point(2,3)
>>>

If omitted, then Point objects would have to be created in a much more clumsy manner
like this:

>>> # Usage if %extend Point is omitted
>>> p1 = sample.Point()
>>> p1.x = 2.0
>>> p1.y = 3

The second customization involving the inclusion of the typemaps.i library and the 
%apply directive is instructing Swig that the argument signature int *remainder is to
be treated as an output value. This is actually a pattern matching rule. In all declarations
that follow, any time  int  *remainder is encountered, it is handled as output. This
customization is what makes the divide() function return two values:

>>> sample.divide(42,8)
[5, 2]
>>>

The last customization involving the %typemap directive is probably the most advanced
feature shown here. A typemap is a rule that gets applied to specific argument patterns
in the input. In this recipe, a typemap has been written to match the argument pattern
(double *a, int n). Inside the typemap is a fragment of C code that tells Swig how
to convert a Python object into the associated C arguments. The code in this recipe has
been written using Python’s buffer protocol in an attempt to match any input argument
that looks like an array of doubles (e.g., NumPy arrays, arrays created by the  array
module, etc.). See Recipe 15.3.
Within the typemap code, substitutions such as $1 and $2 refer to variables that hold
the converted values of the C arguments in the typemap pattern (e.g., $1 maps to double
*a and $2 maps to int n). $input refers to a PyObject * argument that was supplied
as an input argument. $argnum is the argument number.
Writing and understanding typemaps is often the bane of programmers using Swig. Not
only is the code rather cryptic, but you need to understand the intricate details of both
the Python C API and the way in which Swig interacts with it. The Swig documentation
has many more examples and detailed information.
Nevertheless, if you have a lot of a C code to expose as an extension module, Swig can
be a very powerful tool for doing it. The key thing to keep in mind is that Swig is basically
a compiler that processes C declarations, but with a powerful pattern matching and
customization component that lets you change the way in which specific declarations
and types get processed. More information can be found at Swig’s website, including
Python-specific documentation. 

