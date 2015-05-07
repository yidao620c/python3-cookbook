==============================
15.13 传递NULL结尾的字符串给C函数库
==============================

----------
问题
----------
You are writing an extension module that needs to pass a NULL-terminated string to a
C library. However, you’re not entirely sure how to do it with Python’s Unicode string
implementation.

|

----------
解决方案
----------
Many C libraries include functions that operate on NULL-terminated strings declared
as type char *. Consider the following C function that we will use for the purposes of
illustration and testing:

void print_chars(char *s) {
    while (*s) {
        printf("%2x ", (unsigned char) *s);

        s++;
    }
    printf("\n");
}

This function simply prints out the hex representation of individual characters so that
the passed strings can be easily debugged. For example:
print_chars("Hello");   // Outputs: 48 65 6c 6c 6f

For calling such a C function from Python, you have a few choices. First, you could
restrict it to only operate on bytes using "y" conversion code to PyArg_ParseTuple()
like this:

static PyObject *py_print_chars(PyObject *self, PyObject *args) {
  char *s;

  if (!PyArg_ParseTuple(args, "y", &s)) {
    return NULL;
  }
  print_chars(s);
  Py_RETURN_NONE;
}

The resulting function operates as follows. Carefully observe how bytes with embedded
NULL bytes and Unicode strings are rejected:

>>> print_chars(b'Hello World')
48 65 6c 6c 6f 20 57 6f 72 6c 64
>>> print_chars(b'Hello\x00World')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: must be bytes without null bytes, not bytes
>>> print_chars('Hello World')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'str' does not support the buffer interface
>>>

If you want to pass Unicode strings instead, use the "s" format code to PyArg_Parse
Tuple() such as this:

static PyObject *py_print_chars(PyObject *self, PyObject *args) {
  char *s;

  if (!PyArg_ParseTuple(args, "s", &s)) {
    return NULL;
  }
  print_chars(s);
  Py_RETURN_NONE;
}

When used, this will automatically convert all strings to a NULL-terminated UTF-8
encoding. For example:

>>> print_chars('Hello World')
48 65 6c 6c 6f 20 57 6f 72 6c 64
>>> print_chars('Spicy Jalape\u00f1o')  # Note: UTF-8 encoding
53 70 69 63 79 20 4a 61 6c 61 70 65 c3 b1 6f
>>> print_chars('Hello\x00World')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: must be str without null characters, not str
>>> print_chars(b'Hello World')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: must be str, not bytes
>>>

If for some reason, you are working directly with a PyObject * and can’t use PyArg_Par
seTuple(), the following code samples show how you can check and extract a suitable
char * reference, from both a bytes and string object:

/* Some Python Object (obtained somehow) */
PyObject *obj;

/* Conversion from bytes */
{
   char *s;
   s = PyBytes_AsString(o);
   if (!s) {
      return NULL;   /* TypeError already raised */
   }
   print_chars(s);
}

/* Conversion to UTF-8 bytes from a string */
{
   PyObject *bytes;
   char *s;
   if (!PyUnicode_Check(obj)) {
       PyErr_SetString(PyExc_TypeError, "Expected string");
       return NULL;
   }
   bytes = PyUnicode_AsUTF8String(obj);
   s = PyBytes_AsString(bytes);
   print_chars(s);
   Py_DECREF(bytes);
}

Both of the preceding conversions guarantee NULL-terminated data, but they do not
check for embedded NULL bytes elsewhere inside the string. Thus, that’s something
that you would need to check yourself if it’s important.

|

----------
讨论
----------
If it all possible, you should try to avoid writing code that relies on NULL-terminated
strings since Python has no such requirement. It is almost always better to handle strings
using the combination of a pointer and a size if possible. Nevertheless, sometimes you
have to work with legacy C code that presents no other option.
Although it is easy to use, there is a hidden memory overhead associated with using the
"s" format code to PyArg_ParseTuple() that is easy to overlook. When you write code
that uses this conversion, a UTF-8 string is created and permanently attached to the
original string object. If the original string contains non-ASCII characters, this makes
the size of the string increase until it is garbage collected. For example:

>>> import sys
>>> s = 'Spicy Jalape\u00f1o'
>>> sys.getsizeof(s)
87
>>> print_chars(s)     # Passing string
53 70 69 63 79 20 4a 61 6c 61 70 65 c3 b1 6f
>>> sys.getsizeof(s)   # Notice increased size
103
>>>

If this growth in memory use is a concern, you should rewrite your C extension code
to use the PyUnicode_AsUTF8String() function like this:

static PyObject *py_print_chars(PyObject *self, PyObject *args) {
  PyObject *o, *bytes;
  char *s;

  if (!PyArg_ParseTuple(args, "U", &o)) {
    return NULL;
  }
  bytes = PyUnicode_AsUTF8String(o);
  s = PyBytes_AsString(bytes);
  print_chars(s);
  Py_DECREF(bytes);
  Py_RETURN_NONE;
}

With this modification, a UTF-8 encoded string is created if needed, but then discarded
after use. Here is the modified behavior:

>>> import sys
>>> s = 'Spicy Jalape\u00f1o'
>>> sys.getsizeof(s)
87
>>> print_chars(s)
53 70 69 63 79 20 4a 61 6c 61 70 65 c3 b1 6f
>>> sys.getsizeof(s)
87
>>>

If you are trying to pass NULL-terminated strings to functions wrapped via ctypes, be
aware that ctypes only allows bytes to be passed and that it does not check for embedded
NULL bytes. For example:

>>> import ctypes
>>> lib = ctypes.cdll.LoadLibrary("./libsample.so")
>>> print_chars = lib.print_chars
>>> print_chars.argtypes = (ctypes.c_char_p,)
>>> print_chars(b'Hello World')
48 65 6c 6c 6f 20 57 6f 72 6c 64
>>> print_chars(b'Hello\x00World')
48 65 6c 6c 6f
>>> print_chars('Hello World')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ctypes.ArgumentError: argument 1: <class 'TypeError'>: wrong type
>>>

If you want to pass a string instead of bytes, you need to perform a manual UTF-8
encoding first. For example:

>>> print_chars('Hello World'.encode('utf-8'))
48 65 6c 6c 6f 20 57 6f 72 6c 64
>>>

For other extension tools (e.g., Swig, Cython), careful study is probably in order should
you decide to use them to pass strings to C code.
