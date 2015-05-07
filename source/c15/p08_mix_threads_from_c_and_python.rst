==============================
15.8 C和Python中的线程混用
==============================

----------
问题
----------
You have a program that involves a mix of C, Python, and threads, but some of the
threads are created from C outside the control of the Python interpreter. Moreover,
certain threads utilize functions in the Python C API.

Solution
If you’re going to mix C, Python, and threads together, you need to make sure you
properly initialize and manage Python’s global interpreter lock (GIL). To do this, include
the following code somewhere in your C code and make sure it’s called prior to creation
of any threads:

#include <Python.h>

  ...
  if (!PyEval_ThreadsInitialized()) {
    PyEval_InitThreads();
  }
  ...

For any C code that involves Python objects or the Python C API, make sure you prop‐
erly acquire and release the GIL first. This is done using PyGILState_Ensure() and
PyGILState_Release(), as shown in the following:

  ...
  /* Make sure we own the GIL */
  PyGILState_STATE state = PyGILState_Ensure();

  /* Use functions in the interpreter */
  ...
  /* Restore previous GIL state and return */
  PyGILState_Release(state);
  ...

Every  call  to  PyGILState_Ensure()  must  have  a  matching  call  to  PyGILState_Re
lease().

Discussion
In advanced applications involving C and Python, it is not uncommon to have many
things going on at once—possibly involving a mix of a C code, Python code, C threads,
and Python threads. As long as you diligently make sure the interpreter is properly
initialized and that C code involving the interpreter has the proper GIL management
calls, it all should work.
Be aware that the PyGILState_Ensure() call does not immediately preempt or interrupt
the interpreter. If other code is currently executing, this function will block until that
code decides to release the GIL. Internally, the interpreter performs periodic thread
switching, so even if another thread is executing, the caller will eventually get to run
(although it may have to wait for a while first).

