==============================
15.17 传递文件名给C扩展
==============================

----------
问题
----------
You need to pass filenames to C library functions, but need to make sure the filename
has been encoded according to the system’s expected filename encoding.

|

----------
解决方案
----------
To write an extension function that receives a filename, use code such as this:

static PyObject *py_get_filename(PyObject *self, PyObject *args) {
  PyObject *bytes;
  char *filename;
  Py_ssize_t len;
  if (!PyArg_ParseTuple(args,"O&", PyUnicode_FSConverter, &bytes)) {
    return NULL;
  }
  PyBytes_AsStringAndSize(bytes, &filename, &len);
  /* Use filename */
  ...

  /* Cleanup and return */
  Py_DECREF(bytes)
  Py_RETURN_NONE;
}

If you already have a PyObject * that you want to convert as a filename, use code such
as the following:

PyObject *obj;    /* Object with the filename */
PyObject *bytes;
char *filename;
Py_ssize_t len;

bytes = PyUnicode_EncodeFSDefault(obj);
PyBytes_AsStringAndSize(bytes, &filename, &len);
/* Use filename */
...

/* Cleanup */
Py_DECREF(bytes);

If you need to return a filename back to Python, use the following code:

/* Turn a filename into a Python object */

char *filename;       /* Already set */
int   filename_len;   /* Already set */

PyObject *obj = PyUnicode_DecodeFSDefaultAndSize(filename, filename_len);

|

----------
讨论
----------
Dealing with filenames in a portable way is a tricky problem that is best left to Python.
If you use this recipe in your extension code, filenames will be handled in a manner that
is consistent with filename handling in the rest of Python. This includes encoding/
decoding of bytes, dealing with bad characters, surrogate escapes, and other complica‐
tions.
