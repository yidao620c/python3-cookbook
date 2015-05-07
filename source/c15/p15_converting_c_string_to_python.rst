==============================
15.15 C字符串转换为Python字符串
==============================

----------
问题
----------
You want to convert strings from C to Python bytes or a string object.

Solution
For C strings represented as a pair char *, int, you must decide whether or not you
want the string presented as a raw byte string or as a Unicode string. Byte objects can
be built using Py_BuildValue() as follows:

char *s;     /* Pointer to C string data */
int   len;   /* Length of data */

/* Make a bytes object */
PyObject *obj = Py_BuildValue("y#", s, len);

If you want to create a Unicode string and you know that s points to data encoded as
UTF-8, you can use the following:

PyObject *obj = Py_BuildValue("s#", s, len);

If s is encoded in some other known encoding, you can make a string using PyUni
code_Decode() as follows:

PyObject *obj = PyUnicode_Decode(s, len, "encoding", "errors");

/* Examples /*
obj = PyUnicode_Decode(s, len, "latin-1", "strict");
obj = PyUnicode_Decode(s, len, "ascii", "ignore");

If you happen to have a wide string represented as a wchar_t *, len pair, there are a
few options. First, you could use Py_BuildValue() as follows:

wchar_t *w;    /* Wide character string */
int len;       /* Length */

PyObject *obj = Py_BuildValue("u#", w, len);

Alternatively, you can use PyUnicode_FromWideChar():

PyObject *obj = PyUnicode_FromWideChar(w, len);

For wide character strings, no interpretation is made of the character data—it is assumed
to be raw Unicode code points which are directly converted to Python.

Discussion
Conversion of strings from C to Python follow the same principles as I/O. Namely, the
data from C must be explicitly decoded into a string according to some codec. Common
encodings include ASCII, Latin-1, and UTF-8. If you’re not entirely sure of the encoding
or the data is binary, you’re probably best off encoding the string as bytes instead.
When making an object, Python always copies the string data you provide. If necessary,
it’s up to you to release the C string afterward (if required). Also, for better reliability,
you should try to create strings using both a pointer and a size rather than relying on
NULL-terminated data.
