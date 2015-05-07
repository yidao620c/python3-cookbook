==============================
15.19 从C语言中读取类文件对象
==============================

----------
问题
----------
You want to write C extension code that consumes data from any Python file-like object
(e.g., normal files, StringIO objects, etc.).

|

----------
解决方案
----------
To consume data on a file-like object, you need to repeatedly invoke its read() method
and take steps to properly decode the resulting data.
Here is a sample C extension function that merely consumes all of the data on a file-like
object and dumps it to standard output so you can see it:

#define CHUNK_SIZE 8192

/* Consume a "file-like" object and write bytes to stdout */
static PyObject *py_consume_file(PyObject *self, PyObject *args) {
  PyObject *obj;
  PyObject *read_meth;
  PyObject *result = NULL;
  PyObject *read_args;

  if (!PyArg_ParseTuple(args,"O", &obj)) {
    return NULL;
  }

  /* Get the read method of the passed object */
  if ((read_meth = PyObject_GetAttrString(obj, "read")) == NULL) {
    return NULL;
  }

  /* Build the argument list to read() */
  read_args = Py_BuildValue("(i)", CHUNK_SIZE);
  while (1) {
    PyObject *data;
    PyObject *enc_data;
    char *buf;
    Py_ssize_t len;

    /* Call read() */
    if ((data = PyObject_Call(read_meth, read_args, NULL)) == NULL) {
      goto final;
    }

    /* Check for EOF */
    if (PySequence_Length(data) == 0) {
      Py_DECREF(data);
      break;
    }

    /* Encode Unicode as Bytes for C */
    if ((enc_data=PyUnicode_AsEncodedString(data,"utf-8","strict"))==NULL) {
      Py_DECREF(data);
      goto final;
    }

    /* Extract underlying buffer data */
    PyBytes_AsStringAndSize(enc_data, &buf, &len);

    /* Write to stdout (replace with something more useful) */
    write(1, buf, len);

    /* Cleanup */
    Py_DECREF(enc_data);
    Py_DECREF(data);
  }
  result = Py_BuildValue("");

 final:
  /* Cleanup */
  Py_DECREF(read_meth);
  Py_DECREF(read_args);
  return result;
}

To test the code, try making a file-like object such as a StringIO instance and pass it in:

>>> import io
>>> f = io.StringIO('Hello\nWorld\n')
>>> import sample
>>> sample.consume_file(f)
Hello
World
>>>

|

----------
讨论
----------
Unlike a normal system file, a file-like object is not necessarily built around a low-level
file descriptor. Thus, you can’t use normal C library functions to access it. Instead, you
need to use Python’s C API to manipulate the file-like object much like you would in
Python.
In the solution, the read() method is extracted from the passed object. An argument
list is built and then repeatedly passed to PyObject_Call() to invoke the method. To
detect end-of-file (EOF), PySequence_Length() is used to see if the returned result has
zero length.
For all I/O operations, you’ll need to concern yourself with the underlying encoding
and distinction between bytes and Unicode. This recipe shows how to read a file in text
mode and decode the resulting text into a bytes encoding that can be used by C. If you
want to read the file in binary mode, only minor changes will be made. For example:

...
    /* Call read() */
    if ((data = PyObject_Call(read_meth, read_args, NULL)) == NULL) {
      goto final;
    }

    /* Check for EOF */
    if (PySequence_Length(data) == 0) {
      Py_DECREF(data);
      break;
    }
    if (!PyBytes_Check(data)) {
      Py_DECREF(data);
      PyErr_SetString(PyExc_IOError, "File must be in binary mode");
      goto final;
    }

    /* Extract underlying buffer data */
    PyBytes_AsStringAndSize(data, &buf, &len);
    ...

The trickiest part of this recipe concerns proper memory management. When working
with PyObject * variables, careful attention needs to be given to managing reference
counts and cleaning up values when no longer needed. The various Py_DECREF() calls
are doing this.
The recipe is written in a general-purpose manner so that it can be adapted to other file
operations, such as writing. For example, to write data, merely obtain the  write()
method of the file-like object, convert data into an appropriate Python object (bytes or
Unicode), and invoke the method to have it written to the file.
Finally,  although  file-like  objects  often  provide  other  methods  (e.g.,  readline(),
read_into()), it is probably best to just stick with the basic read() and write() meth‐
ods for maximal portability. Keeping things as simple as possible is often a good policy
for C extensions.
