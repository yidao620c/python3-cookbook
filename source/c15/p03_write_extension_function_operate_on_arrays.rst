==============================
15.3 一个操作数组的扩展函数
==============================

----------
问题
----------
You want to write a C extension function that operates on contiguous arrays of data, as
might be created by the array module or libraries like NumPy. However, you would like
your function to be general purpose and not specific to any one array library.

Solution
To receive and process arrays in a portable manner, you should write code that uses the
Buffer Protocol. Here is an example of a handwritten C extension function that receives
array data and calls the avg(double *buf, int len) function from this chapter’s in‐
troduction:

/* Call double avg(double *, int) */
static PyObject *py_avg(PyObject *self, PyObject *args) {
  PyObject *bufobj;
  Py_buffer view;
  double result;
  /* Get the passed Python object */
  if (!PyArg_ParseTuple(args, "O", &bufobj)) {
    return NULL;
  }

  /* Attempt to extract buffer information from it */

  if (PyObject_GetBuffer(bufobj, &view,
      PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT) == -1) {
    return NULL;
  }

  if (view.ndim != 1) {
    PyErr_SetString(PyExc_TypeError, "Expected a 1-dimensional array");
    PyBuffer_Release(&view);
    return NULL;
  }

  /* Check the type of items in the array */
  if (strcmp(view.format,"d") != 0) {
    PyErr_SetString(PyExc_TypeError, "Expected an array of doubles");
    PyBuffer_Release(&view);
    return NULL;
  }

  /* Pass the raw buffer and size to the C function */
  result = avg(view.buf, view.shape[0]);

  /* Indicate we're done working with the buffer */
  PyBuffer_Release(&view);
  return Py_BuildValue("d", result);
}

Here is an example that shows how this extension function works:

>>> import array
>>> avg(array.array('d',[1,2,3]))
2.0
>>> import numpy
>>> avg(numpy.array([1.0,2.0,3.0]))
2.0
>>> avg([1,2,3])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'list' does not support the buffer interface
>>> avg(b'Hello')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: Expected an array of doubles
>>> a = numpy.array([[1.,2.,3.],[4.,5.,6.]])
>>> avg(a[:,2])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: ndarray is not contiguous
>>> sample.avg(a)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: Expected a 1-dimensional array
>>> sample.avg(a[0])

2.0
>>>

Discussion
Passing array objects to C functions might be one of the most common things you would
want to do with a extension function. A large number of Python applications, ranging
from image processing to scientific computing, are based on high-performance array
processing. By writing code that can accept and operate on arrays, you can write cus‐
tomized code that plays nicely with those applications as opposed to having some sort
of custom solution that only works with your own code.
The key to this code is the PyBuffer_GetBuffer() function. Given an arbitrary Python
object, it tries to obtain information about the underlying memory representation. If
it’s not possible, as is the case with most normal Python objects, it simply raises an
exception  and  returns  -1.  The  special  flags  passed  to  PyBuffer_GetBuffer()  give
additional  hints  about  the  kind  of  memory  buffer  that  is  requested.  For  example,
PyBUF_ANY_CONTIGUOUS specifies that a contiguous region of memory is required.
For arrays, byte strings, and other similar objects, a Py_buffer structure is filled with
information about the underlying memory. This includes a pointer to the memory, size,
itemsize, format, and other details. Here is the definition of this structure:

typedef struct bufferinfo {
    void *buf;              /* Pointer to buffer memory */
    PyObject *obj;          /* Python object that is the owner */
    Py_ssize_t len;         /* Total size in bytes */
    Py_ssize_t itemsize;    /* Size in bytes of a single item */
    int readonly;           /* Read-only access flag */
    int ndim;               /* Number of dimensions */
    char *format;           /* struct code of a single item */
    Py_ssize_t *shape;      /* Array containing dimensions */
    Py_ssize_t *strides;    /* Array containing strides */
    Py_ssize_t *suboffsets; /* Array containing suboffsets */
} Py_buffer;

In this recipe, we are simply concerned with receiving a contiguous array of doubles.
To check if items are a double, the format attribute is checked to see if the string is
"d". This is the same code that the struct module uses when encoding binary values.
As a general rule, format could be any format string that’s compatible with the struct
module and might include multiple items in the case of arrays containing C structures.
Once we have verified the underlying buffer information, we simply pass it to the C
function, which treats it as a normal C array. For all practical purposes, it is not con‐
cerned with what kind of array it is or what library created it. This is how the function
is able to work with arrays created by the array module or by numpy.

Before  returning  a  final  result,  the  underlying  buffer  view  must  be  released  using 
PyBuffer_Release(). This step is required to properly manage reference counts of
objects.
Again, this recipe only shows a tiny fragment of code that receives an array. If working
with arrays, you might run into issues with multidimensional data, strided data, different
data types, and more that will require study. Make sure you consult the official docu‐
mentation to get more details.
If you need to write many extensions involving array handling, you may find it easier
to implement the code in Cython. See Recipe 15.11. 
