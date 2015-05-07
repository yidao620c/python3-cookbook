==============================
15.20 处理C语言中的可迭代对象
==============================

----------
问题
----------
You want to write C extension code that consumes items from any iterable object such
as a list, tuple, file, or generator.

Solution
Here is a sample C extension function that shows how to consume the items on an
iterable:

static PyObject *py_consume_iterable(PyObject *self, PyObject *args) {
  PyObject *obj;
  PyObject *iter;
  PyObject *item;

  if (!PyArg_ParseTuple(args, "O", &obj)) {
    return NULL;
  }
  if ((iter = PyObject_GetIter(obj)) == NULL) {
    return NULL;
  }
  while ((item = PyIter_Next(iter)) != NULL) {
    /* Use item */
    ...
    Py_DECREF(item);
  }

  Py_DECREF(iter);
  return Py_BuildValue("");
}

Discussion
The code in this recipe mirrors similar code in Python. The PyObject_GetIter() call
is the same as calling iter() to get an iterator. The PyIter_Next() function invokes
the next method on the iterator returning the next item or NULL if there are no more
items. Make sure you’re careful with memory management—Py_DECREF() needs to be
called on both the produced items and the iterator object itself to avoid leaking memory.
