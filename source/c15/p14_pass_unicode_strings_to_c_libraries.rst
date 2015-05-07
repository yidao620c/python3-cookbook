==============================
15.14 传递Unicode字符串给C函数库
==============================

----------
问题
----------
You are writing an extension module that needs to pass a Python string to a C library
function that may or may not know how to properly handle Unicode.

Solution
There are many issues to be concerned with here, but the main one is that existing C
libraries won’t understand Python’s native representation of Unicode. Therefore, your
challenge is to convert the Python string into a form that can be more easily understood
by C libraries.
For the purposes of illustration, here are two C functions that operate on string data
and output it for the purposes of debugging and experimentation. One uses bytes pro‐
vided in the form char *, int, whereas the other uses wide characters in the form
wchar_t *, int:

void print_chars(char *s, int len) {
  int n = 0;

  while (n < len) {
    printf("%2x ", (unsigned char) s[n]);
    n++;
  }
  printf("\n");
}

void print_wchars(wchar_t *s, int len) {
  int n = 0;
  while (n < len) {
    printf("%x ", s[n]);
    n++;
  }
  printf("\n");
}

For the byte-oriented function print_chars(), you need to convert Python strings into
a suitable byte encoding such as UTF-8. Here is a sample extension function that does
this:

static PyObject *py_print_chars(PyObject *self, PyObject *args) {
  char *s;
  Py_ssize_t  len;

  if (!PyArg_ParseTuple(args, "s#", &s, &len)) {
    return NULL;
  }
  print_chars(s, len);
  Py_RETURN_NONE;
}

For library functions that work with the machine native wchar_t type, you can write
extension code such as this:

static PyObject *py_print_wchars(PyObject *self, PyObject *args) {
  wchar_t *s;
  Py_ssize_t  len;

  if (!PyArg_ParseTuple(args, "u#", &s, &len)) {
    return NULL;
  }
  print_wchars(s,len);
  Py_RETURN_NONE;
}

Here is an interactive session that illustrates how these functions work:

>>> s = 'Spicy Jalape\u00f1o'
>>> print_chars(s)
53 70 69 63 79 20 4a 61 6c 61 70 65 c3 b1 6f
>>> print_wchars(s)
53 70 69 63 79 20 4a 61 6c 61 70 65 f1 6f
>>>

Carefully observe how the byte-oriented function print_chars() is receiving UTF-8
encoded data, whereas print_wchars() is receiving the Unicode code point values.

Discussion
Before considering this recipe, you should first study the nature of the C library that
you’re accessing. For many C libraries, it might make more sense to pass bytes instead
of a string. To do that, use this conversion code instead:

static PyObject *py_print_chars(PyObject *self, PyObject *args) {
  char *s;
  Py_ssize_t  len;

  /* accepts bytes, bytearray, or other byte-like object */
  if (!PyArg_ParseTuple(args, "y#", &s, &len)) {
    return NULL;
  }
  print_chars(s, len);
  Py_RETURN_NONE;
}

If you decide that you still want to pass strings, you need to know that Python 3 uses an
adaptable string representation that is not entirely straightforward to map directly to C
libraries using the standard types char * or wchar_t * See PEP 393 for details. Thus,
to present string data to C, some kind of conversion is almost always necessary. The s#
and u# format codes to PyArg_ParseTuple() safely perform such conversions.
One potential downside is that such conversions cause the size of the original string
object to permanently increase. Whenever a conversion is made, a copy of the converted
data is kept and attached to the original string object so that it can be reused later. You
can observe this effect:

>>> import sys
>>> s = 'Spicy Jalape\u00f1o'
>>> sys.getsizeof(s)
87
>>> print_chars(s)
53 70 69 63 79 20 4a 61 6c 61 70 65 c3 b1 6f
>>> sys.getsizeof(s)
103
>>> print_wchars(s)
53 70 69 63 79 20 4a 61 6c 61 70 65 f1 6f
>>> sys.getsizeof(s)
163
>>>

For small amounts of string data, this might not matter, but if you’re doing large amounts
of  text  processing  in  extensions,  you  may  want  to  avoid  the  overhead.  Here  is  an
alternative implementation of the first extension function that avoids these memory
inefficiencies:

static PyObject *py_print_chars(PyObject *self, PyObject *args) {
  PyObject *obj, *bytes;
  char *s;
  Py_ssize_t   len;

  if (!PyArg_ParseTuple(args, "U", &obj)) {
    return NULL;
  }
  bytes = PyUnicode_AsUTF8String(obj);
  PyBytes_AsStringAndSize(bytes, &s, &len);
  print_chars(s, len);
  Py_DECREF(bytes);
  Py_RETURN_NONE;
}

Avoiding  memory  overhead  for  wchar_t  handling  is  much  more  tricky.  Internally,
Python stores strings using the most efficient representation possible. For example,
strings containing nothing but ASCII are stored as arrays of bytes, whereas strings con‐
taining characters in the range U+0000 to U+FFFF use a two-byte representation. Since
there isn’t a single representation of the data, you can’t just cast the internal array to
wchar_t * and hope that it works. Instead, a wchar_t array has to be created and text
copied into it. The "u#" format code to PyArg_ParseTuple() does this for you at the
cost of efficiency (it attaches the resulting copy to the string object).
If you want to avoid this long-term memory overhead, your only real choice is to copy
the Unicode data into a temporary array, pass it to the C library function, and then
deallocate the array. Here is one possible implementation:

static PyObject *py_print_wchars(PyObject *self, PyObject *args) {
  PyObject *obj;
  wchar_t *s;
  Py_ssize_t len;

  if (!PyArg_ParseTuple(args, "U", &obj)) {
    return NULL;
  }
  if ((s = PyUnicode_AsWideCharString(obj, &len)) == NULL) {
    return NULL;
  }
  print_wchars(s, len);
  PyMem_Free(s);
  Py_RETURN_NONE;
}

In this implementation, PyUnicode_AsWideCharString() creates a temporary buffer of
wchar_t characters and copies data into it. That buffer is passed to C and then released
afterward. As of this writing, there seems to be a possible bug related to this behavior,
as described at the Python issues page.

If, for some reason you know that the C library takes the data in a different byte encoding
than UTF-8, you can force Python to perform an appropriate conversion using exten‐
sion code such as the following:

static PyObject *py_print_chars(PyObject *self, PyObject *args) {
  char *s = 0;
  int   len;
  if (!PyArg_ParseTuple(args, "es#", "encoding-name", &s, &len)) {
    return NULL;
  }
  print_chars(s, len);
  PyMem_Free(s);
  Py_RETURN_NONE;
}

Last, but not least, if you want to work directly with the characters in a Unicode string,
here is an example that illustrates low-level access:

static PyObject *py_print_wchars(PyObject *self, PyObject *args) {
  PyObject *obj;
  int n, len;
  int kind;
  void *data;

  if (!PyArg_ParseTuple(args, "U", &obj)) {
    return NULL;
  }
  if (PyUnicode_READY(obj) < 0) {
    return NULL;
  }

  len = PyUnicode_GET_LENGTH(obj);
  kind = PyUnicode_KIND(obj);
  data = PyUnicode_DATA(obj);

  for (n = 0; n < len; n++) {
    Py_UCS4 ch = PyUnicode_READ(kind, data, n);
    printf("%x ", ch);
  }
  printf("\n");
  Py_RETURN_NONE;
}

In this code, the PyUnicode_KIND() and PyUnicode_DATA() macros are related to the
variable-width storage of Unicode, as described in PEP 393. The kind variable encodes
information about the underlying storage (8-bit, 16-bit, or 32-bit) and data points the
buffer. In reality, you don’t need to do anything with these values as long as you pass
them to the PyUnicode_READ() macro when extracting characters.
A few final words: when passing Unicode strings from Python to C, you should probably
try to make it as simple as possible. If given the choice between an encoding such as

UTF-8 or wide characters, choose UTF-8. Support for UTF-8 seems to be much more
common, less trouble-prone, and better supported by the interpreter. Finally, make sure
your review the documentation on Unicode handling. 
