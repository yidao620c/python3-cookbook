==============================
15.16 不确定编码格式的C字符串
==============================

----------
问题
----------
You are converting strings back and forth between C and Python, but the C encoding
is of a dubious or unknown nature. For example, perhaps the C data is supposed to be
UTF-8, but it’s not being strictly enforced. You would like to write code that can handle
malformed data in a graceful way that doesn’t crash Python or destroy the string data
in the process.

|

----------
解决方案
----------
Here is some C data and a function that illustrates the nature of this problem:

/* Some dubious string data (malformed UTF-8) */
const char *sdata = "Spicy Jalape\xc3\xb1o\xae";
int slen = 16;

/* Output character data */
void print_chars(char *s, int len) {
  int n = 0;
  while (n < len) {
    printf("%2x ", (unsigned char) s[n]);
    n++;
  }
  printf("\n");
}

In this code, the string sdata contains a mix of UTF-8 and malformed data. Neverthe‐
less, if a user calls print_chars(sdata, slen) in C, it works fine.
Now suppose you want to convert the contents of sdata into a Python string. Further
suppose you want to later pass that string to the print_chars() function through an
extension. Here’s how to do it in a way that exactly preserves the original data even
though there are encoding problems:

/* Return the C string back to Python */
static PyObject *py_retstr(PyObject *self, PyObject *args) {
  if (!PyArg_ParseTuple(args, "")) {
    return NULL;
  }
  return PyUnicode_Decode(sdata, slen, "utf-8", "surrogateescape");
}

/* Wrapper for the print_chars() function */
static PyObject *py_print_chars(PyObject *self, PyObject *args) {
  PyObject *obj, *bytes;
  char *s = 0;
  Py_ssize_t   len;

  if (!PyArg_ParseTuple(args, "U", &obj)) {
    return NULL;
  }

  if ((bytes = PyUnicode_AsEncodedString(obj,"utf-8","surrogateescape"))
        == NULL) {
    return NULL;
  }
  PyBytes_AsStringAndSize(bytes, &s, &len);
  print_chars(s, len);
  Py_DECREF(bytes);
  Py_RETURN_NONE;
}

If you try these functions from Python, here’s what happens:

>>> s = retstr()
>>> s
'Spicy Jalapeño\udcae'
>>> print_chars(s)
53 70 69 63 79 20 4a 61 6c 61 70 65 c3 b1 6f ae
>>>

Careful observation will reveal that the malformed string got encoded into a Python
string without errors, and that when passed back into C, it turned back into a byte string
that exactly encoded the same bytes as the original C string.

|

----------
讨论
----------
This recipe addresses a subtle, but potentially annoying problem with string handling
in extension modules. Namely, the fact that C strings in extensions might not follow the
strict Unicode encoding/decoding rules that Python normally expects. Thus, it’s possible
that some malformed C data would pass to Python. A good example might be C strings
associated with low-level system calls such as filenames. For instance, what happens if
a  system  call  returns  a  broken  string  back  to  the  interpreter  that  can’t  be  properly
decoded.

Normally, Unicode errors are often handled by specifying some sort of error policy, such
as strict, ignore, replace, or something similar. However, a downside of these policies
is that they irreparably destroy the original string content. For example, if the malformed
data in the example was decoded using one of these polices, you would get results such
as this:

>>> raw = b'Spicy Jalape\xc3\xb1o\xae'
>>> raw.decode('utf-8','ignore')
'Spicy Jalapeño'
>>> raw.decode('utf-8','replace')
'Spicy Jalapeño?'
>>>

The surrogateescape error handling policies takes all nondecodable bytes and turns
them into the low-half of a surrogate pair (\udcXX where XX is the raw byte value). For
example:

>>> raw.decode('utf-8','surrogateescape')
'Spicy Jalapeño\udcae'
>>>

Isolated low surrogate characters such as \udcae never appear in valid Unicode. Thus,
this string is technically an illegal representation. In fact, if you ever try to pass it to
functions that perform output, you’ll get encoding errors:

>>> s = raw.decode('utf-8', 'surrogateescape')
>>> print(s)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeEncodeError: 'utf-8' codec can't encode character '\udcae'
in position 14: surrogates not allowed
>>>

However, the main point of allowing the surrogate escapes is to allow malformed strings
to pass from C to Python and back into C without any data loss. When the string is
encoded using surrogateescape again, the surrogate characters are turned back into
their original bytes. For example:

>>> s
'Spicy Jalapeño\udcae'
>>> s.encode('utf-8','surrogateescape')
b'Spicy Jalape\xc3\xb1o\xae'
>>>

As a general rule, it’s probably best to avoid surrogate encoding whenever possible—
your code will be much more reliable if it uses proper encodings. However, sometimes
there are situations where you simply don’t have control over the data encoding and
you aren’t free to ignore or replace the bad data because other functions may need to
use it. This recipe shows how to do it.

As a final note, many of Python’s system-oriented functions, especially those related to
filenames, environment variables, and command-line options, use surrogate encoding.
For example, if you use a function such as os.listdir() on a directory containing a
undecodable  filename,  it  will  be  returned  as  a  string  with  surrogate  escapes.  See
Recipe 5.15 for a related recipe.
PEP 383 has more information about the problem addressed by this recipe and surro
gateescape error handling.
