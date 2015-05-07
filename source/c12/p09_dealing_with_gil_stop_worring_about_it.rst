============================
12.9 Python的全局锁问题
============================

----------
问题
----------
You’ve heard about the Global Interpreter Lock (GIL), and are worried that it might be
affecting the performance of your multithreaded program.

Solution
Although Python fully supports thread programming, parts of the C implementation
of the interpreter are not entirely thread safe to a level of allowing fully concurrent
execution. In fact, the interpreter is protected by a so-called Global Interpreter Lock
(GIL) that only allows one Python thread to execute at any given time. The most no‐
ticeable effect of the GIL is that multithreaded Python programs are not able to fully
take advantage of multiple CPU cores (e.g., a computationally intensive application
using more than one thread only runs on a single CPU).

Before discussing common GIL workarounds, it is important to emphasize that the GIL
tends to only affect programs that are heavily CPU bound (i.e., dominated by compu‐
tation). If your program is mostly doing I/O, such as network communication, threads
are often a sensible choice because they’re mostly going to spend their time sitting
around waiting. In fact, you can create thousands of Python threads with barely a con‐
cern. Modern operating systems have no trouble running with that many threads, so
it’s simply not something you should worry much about.
For CPU-bound programs, you really need to study the nature of the computation being
performed. For instance, careful choice of the underlying algorithm may produce a far
greater speedup than trying to parallelize an unoptimal algorithm with threads. Simi‐
larly, given that Python is interpreted, you might get a far greater speedup simply by
moving  performance-critical  code  into  a  C  extension  module.  Extensions  such  as 
NumPy are also highly effective at speeding up certain kinds of calculations involving
array data. Last, but not least, you might investigate alternative implementations, such
as PyPy, which features optimizations such as a JIT compiler (although, as of this writing,
it does not yet support Python 3).
It’s also worth noting that threads are not necessarily used exclusively for performance.
A CPU-bound program might be using threads to manage a graphical user interface, a
network connection, or provide some other kind of service. In this case, the GIL can
actually present more of a problem, since code that holds it for an excessively long period
will cause annoying stalls in the non-CPU-bound threads. In fact, a poorly written C
extension can actually make this problem worse, even though the computation part of
the code might run faster than before.
Having said all of this, there are two common strategies for working around the limi‐
tations of the GIL. First, if you are working entirely in Python, you can use the multi
processing module to create a process pool and use it like a co-processor. For example,
suppose you have the following thread code:

# Performs a large calculation (CPU bound)
def some_work(args):
    ...
    return result

# A thread that calls the above function
def some_thread():
    while True:
        ...
        r = some_work(args)
        ...

Here’s how you would modify the code to use a pool:

# Processing pool (see below for initiazation)
pool = None

# Performs a large calculation (CPU bound)
def some_work(args):
    ...
    return result

# A thread that calls the above function
def some_thread():
    while True:
        ...
        r = pool.apply(some_work, (args))
        ...

# Initiaze the pool
if __name__ == '__main__':
    import multiprocessing
    pool = multiprocessing.Pool()

This example with a pool works around the GIL using a neat trick. Whenever a thread
wants to perform CPU-intensive work, it hands the work to the pool. The pool, in turn,
hands the work to a separate Python interpreter running in a different process. While
the thread is waiting for the result, it releases the GIL. Moreover, because the calculation
is being performed in a separate interpreter, it’s no longer bound by the restrictions of
the GIL. On a multicore system, you’ll find that this technique easily allows you to take
advantage of all the CPUs.
The second strategy for working around the GIL is to focus on C extension program‐
ming. The general idea is to move computationally intensive tasks to C, independent of
Python, and have the C code release the GIL while it’s working. This is done by inserting
special macros into the C code like this:

#include "Python.h"
...

PyObject *pyfunc(PyObject *self, PyObject *args) {
   ...
   Py_BEGIN_ALLOW_THREADS
   // Threaded C code
   ...
   Py_END_ALLOW_THREADS
   ...
}

If you are using other tools to access C, such as the ctypes library or Cython, you may
not need to do anything. For example, ctypes releases the GIL when calling into C by
default.

Discussion
Many programmers, when faced with thread performance problems, are quick to blame
the GIL for all of their ills. However, doing so is shortsighted and naive. Just as a real-

world example, mysterious “stalls” in a multithreaded network program might be caused
by something entirely different (e.g., a stalled DNS lookup) rather than anything related
to the GIL. The bottom line is that you really need to study your code to know if the
GIL is an issue or not. Again, realize that the GIL is mostly concerned with CPU-bound
processing, not I/O.
If you are going to use a process pool as a workaround, be aware that doing so involves
data serialization and communication with a different Python interpreter. For this to
work, the operation to be performed needs to be contained within a Python function
defined by the def statement (i.e., no lambdas, closures, callable instances, etc.), and the
function arguments and return value must be compatible with pickle. Also, the amount
of work to be performed must be sufficiently large to make up for the extra communi‐
cation overhead.
Another subtle aspect of pools is that mixing threads and process pools together can be
a good way to make your head explode. If you are going to use both of these features
together, it is often best to create the process pool as a singleton at program startup,
prior to the creation of any threads. Threads will then use the same process pool for all
of their computationally intensive work.
For C extensions, the most important feature is maintaining isolation from the Python
interpreter process. That is, if you’re going to offload work from Python to C, you need
to make sure the C code operates independently of Python. This means using no Python
data structures and making no calls to Python’s C API. Another consideration is that
you want to make sure your C extension does enough work to make it all worthwhile.
That is, it’s much better if the extension can perform millions of calculations as opposed
to just a few small calculations.
Needless to say, these solutions to working around the GIL don’t apply to all possible
problems. For instance, certain kinds of applications don’t work well if separated into
multiple processes, nor may you want to code parts in C. For these kinds of applications,
you may have to come up with your own solution (e.g., multiple processes accessing
shared memory regions, multiple interpreters running in the same process, etc.). Al‐
ternatively, you might look at some other implementations of the interpreter, such as
PyPy.
See  Recipes  15.7  and  15.10  for  additional  information  on  releasing  the  GIL  in  C
extensions.
