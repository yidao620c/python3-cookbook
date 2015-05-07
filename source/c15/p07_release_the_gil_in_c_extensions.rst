==============================
15.7 从C扩展中释放全局锁
==============================

----------
问题
----------
You have C extension code in that you want to execute concurrently with other threads
in the Python interpreter. To do this, you need to release and reacquire the global in‐
terpreter lock (GIL).

Solution
In C extension code, the GIL can be released and reacquired by inserting the following
macros in the code:

#include "Python.h"
...

PyObject *pyfunc(PyObject *self, PyObject *args) {
   ...
   Py_BEGIN_ALLOW_THREADS
   // Threaded C code.  Must not use Python API functions
   ...
   Py_END_ALLOW_THREADS
   ...
   return result;
}

Discussion
The GIL can only safely be released if you can guarantee that no Python C API functions
will be executed in the C code. Typical examples where the GIL might be released are
in computationally intensive code that performs calculations on C arrays (e.g., in ex‐
tensions such as numpy) or in code where blocking I/O operations are going to be per‐
formed (e.g., reading or writing on a file descriptor).
While the GIL is released, other Python threads are allowed to execute in the interpreter.
The Py_END_ALLOW_THREADS macro blocks execution until the calling threads reacquires
the GIL in the interpreter.
