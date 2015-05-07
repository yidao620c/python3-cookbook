==============================
15.6 从C语言中调用Python代码
==============================

----------
问题
----------
You want to safely execute a Python callable from C and return a result back to C. For
example, perhaps you are writing C code that wants to use a Python function as a
callback.

|

----------
解决方案
----------
Calling Python from C is mostly straightforward, but involves a number of tricky parts.
The following C code shows an example of how to do it safely:

#include <Python.h>

/* Execute func(x,y) in the Python interpreter.  The
   arguments and return result of the function must
   be Python floats */

double call_func(PyObject *func, double x, double y) {
  PyObject *args;
  PyObject *kwargs;
  PyObject *result = 0;
  double retval;

  /* Make sure we own the GIL */
  PyGILState_STATE state = PyGILState_Ensure();

  /* Verify that func is a proper callable */
  if (!PyCallable_Check(func)) {
    fprintf(stderr,"call_func: expected a callable\n");
    goto fail;
  }
  /* Build arguments */
  args = Py_BuildValue("(dd)", x, y);
  kwargs = NULL;

  /* Call the function */
  result = PyObject_Call(func, args, kwargs);
  Py_DECREF(args);
  Py_XDECREF(kwargs);

  /* Check for Python exceptions (if any) */
  if (PyErr_Occurred()) {
    PyErr_Print();
    goto fail;
  }

  /* Verify the result is a float object */
  if (!PyFloat_Check(result)) {
    fprintf(stderr,"call_func: callable didn't return a float\n");
    goto fail;
  }

  /* Create the return value */
  retval = PyFloat_AsDouble(result);
  Py_DECREF(result);

  /* Restore previous GIL state and return */
  PyGILState_Release(state);
  return retval;

fail:
  Py_XDECREF(result);
  PyGILState_Release(state);
  abort();   // Change to something more appropriate
}

To use this function, you need to have obtained a reference to an existing Python callable
to pass in. There are many ways that you can go about doing that, such as having a
callable object passed into an extension module or simply writing C code to extract a
symbol from an existing module.
Here is a simple example that shows calling a function from an embedded Python
interpreter:

#include <Python.h>

/* Definition of call_func() same as above */
...

/* Load a symbol from a module */
PyObject *import_name(const char *modname, const char *symbol) {
  PyObject *u_name, *module;
  u_name = PyUnicode_FromString(modname);
  module = PyImport_Import(u_name);
  Py_DECREF(u_name);
  return PyObject_GetAttrString(module, symbol);
}

/* Simple embedding example */
int main() {
  PyObject *pow_func;
  double x;

  Py_Initialize();
  /* Get a reference to the math.pow function */
  pow_func = import_name("math","pow");

  /* Call it using our call_func() code */
  for (x = 0.0; x < 10.0; x += 0.1) {
    printf("%0.2f %0.2f\n", x, call_func(pow_func,x,2.0));
  }
  /* Done */
  Py_DECREF(pow_func);
  Py_Finalize();
  return 0;
}

To build this last example, you’ll need to compile the C and link against the Python
interpreter. Here is a Makefile that shows how you might do it (this is something that
might require some amount of fiddling with on your machine):

all::
        cc -g embed.c -I/usr/local/include/python3.3m \
          -L/usr/local/lib/python3.3/config-3.3m -lpython3.3m

Compiling and running the resulting executable should produce output similar to this:

0.00 0.00
0.10 0.01
0.20 0.04
0.30 0.09
0.40 0.16
...

Here is a slightly different example that shows an extension function that receives a
callable  and  some  arguments  and  passes  them  to  call_func()  for  the  purposes  of
testing:

/* Extension function for testing the C-Python callback */
PyObject *py_call_func(PyObject *self, PyObject *args) {
  PyObject *func;

  double x, y, result;
  if (!PyArg_ParseTuple(args,"Odd", &func,&x,&y)) {
    return NULL;
  }
  result = call_func(func, x, y);
  return Py_BuildValue("d", result);
}

Using this extension function, you could test it as follows:

>>> import sample
>>> def add(x,y):
...     return x+y
...
>>> sample.call_func(add,3,4)
7.0
>>>

|

----------
讨论
----------
If you are calling Python from C, the most important thing to keep in mind is that C is
generally going to be in charge. That is, C has the responsibility of creating the argu‐
ments, calling the Python function, checking for exceptions, checking types, extracting
return values, and more.
As a first step, it is critical that you have a Python object representing the callable that
you’re going to invoke. This could be a function, class, method, built-in method, or
anything that implements the __call__() operation. To verify that it’s callable, use 
PyCallable_Check() as shown in this code fragment:

double call_func(PyObject *func, double x, double y) {
  ...
  /* Verify that func is a proper callable */
  if (!PyCallable_Check(func)) {
    fprintf(stderr,"call_func: expected a callable\n");
    goto fail;
  }
  ...

As an aside, handling errors in the C code is something that you will need to carefully
study. As a general rule, you can’t just raise a Python exception. Instead, errors will have
to be handled in some other manner that makes sense to your C code. In the solution,
we’re using goto to transfer control to an error handling block that calls abort(). This
causes the whole program to die, but in real code you would probably want to do some‐
thing more graceful (e.g., return a status code). Keep in mind that C is in charge here,
so there isn’t anything comparable to just raising an exception. Error handling is some‐
thing you’ll have to engineer into the program somehow.
Calling a function is relatively straightforward—simply use PyObject_Call(), supply‐
ing  it  with  the  callable  object,  a  tuple  of  arguments,  and  an  optional  dictionary  of

keyword arguments. To build the argument tuple or dictionary, you can use Py_Build
Value(), as shown.

double call_func(PyObject *func, double x, double y) {
  PyObject *args;
  PyObject *kwargs;

  ...
  /* Build arguments */
  args = Py_BuildValue("(dd)", x, y);
  kwargs = NULL;

  /* Call the function */
  result = PyObject_Call(func, args, kwargs);
  Py_DECREF(args);
  Py_XDECREF(kwargs);
  ...

If there are no keyword arguments, you can pass NULL, as shown. After making the
function call, you need to make sure that you clean up the arguments using  Py_DE
CREF() or  Py_XDECREF(). The latter function safely allows the NULL pointer to be
passed (which is ignored), which is why we’re using it for cleaning up the optional
keyword arguments.
After calling the Python function, you must check for the presence of exceptions. The 
PyErr_Occurred() function can be used to do this. Knowing what to do in response to
an exception is tricky. Since you’re working from C, you really don’t have the exception
machinery that Python has. Thus, you would have to set an error status code, log the
error, or do some kind of sensible processing. In the solution, abort() is called for lack
of a simpler alternative (besides, hardened C programmers will appreciate the abrupt
crash):

  ...
  /* Check for Python exceptions (if any) */
  if (PyErr_Occurred()) {
    PyErr_Print();
    goto fail;
  }
  ...
fail:
  PyGILState_Release(state);
  abort();

Extracting information from the return value of calling a Python function is typically
going to involve some kind of type checking and value extraction. To do this, you may
have to use functions in the Python concrete objects layer. In the solution, the code
checks for and extracts the value of a Python float using  PyFloat_Check() and  Py
Float_AsDouble().

A final tricky part of calling into Python from C concerns the management of Python’s
global interpreter lock (GIL). Whenever Python is accessed from C, you need to make
sure that the GIL is properly acquired and released. Otherwise, you run the risk of having
the interpreter corrupt data or crash. The calls to  PyGILState_Ensure() and  PyGIL
State_Release() make sure that it’s done correctly:

double call_func(PyObject *func, double x, double y) {
  ...
  double retval;

  /* Make sure we own the GIL */
  PyGILState_STATE state = PyGILState_Ensure();
  ...
  /* Code that uses Python C API functions */
  ...
  /* Restore previous GIL state and return */
  PyGILState_Release(state);
  return retval;

fail:
  PyGILState_Release(state);
  abort();
}

Upon return, PyGILState_Ensure() always guarantees that the calling thread has ex‐
clusive access to the Python interpreter. This is true even if the calling C code is running
a different thread that is unknown to the interpreter. At this point, the C code is free to
use any Python C-API functions that it wants. Upon successful completion,  PyGIL
State_Release() is used to restore the interpreter back to its original state.
It is critical to note that every PyGILState_Ensure() call must be followed by a matching
PyGILState_Release() call—even in cases where errors have occurred. In the solution,
the use of a goto statement might look like a horrible design, but we’re actually using it
to transfer control to a common exit block that performs this required step. Think of
the code after the fail: lable as serving the same purpose as code in a Python final
ly: block.
If you write your C code using all of these conventions including management of the
GIL, checking for exceptions, and thorough error checking, you’ll find that you can
reliably call into the Python interpreter from C—even in very complicated programs
that utilize advanced programming techniques such as multithreading.

