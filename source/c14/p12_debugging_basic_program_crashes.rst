==============================
14.12 调试基本的程序崩溃错误
==============================

----------
问题
----------
Your program is broken and you’d like some simple strategies for debugging it.

|

----------
解决方案
----------
If your program is crashing with an exception, running your program as python3 -i
someprogram.py can be a useful tool for simply looking around. The -i option starts
an interactive shell as soon as a program terminates. From there, you can explore the
environment. For example, suppose you have this code:

# sample.py

def func(n):
    return n + 10

func('Hello')

Running python3 -i produces the following:

bash % python3 -i sample.py
Traceback (most recent call last):
  File "sample.py", line 6, in <module>
    func('Hello')
  File "sample.py", line 4, in func
    return n + 10
TypeError: Can't convert 'int' object to str implicitly
>>> func(10)
20
>>>

If you don’t see anything obvious, a further step is to launch the Python debugger after
a crash. For example:

>>> import pdb
>>> pdb.pm()
> sample.py(4)func()
-> return n + 10
(Pdb) w
  sample.py(6)<module>()
-> func('Hello')
> sample.py(4)func()
-> return n + 10
(Pdb) print n
'Hello'
(Pdb) q
>>>

If your code is deeply buried in an environment where it is difficult to obtain an inter‐
active shell (e.g., in a server), you can often catch errors and produce tracebacks yourself.
For example:

import traceback
import sys

try:
    func(arg)
except:
    print('**** AN ERROR OCCURRED ****')
    traceback.print_exc(file=sys.stderr)

If your program isn’t crashing, but it’s producing wrong answers or you’re mystified by
how it works, there is often nothing wrong with just injecting a few print() calls in
places of interest. However, if you’re going to do that, there are a few related techniques
of interest. First, the traceback.print_stack() function will create a stack track of
your program immediately at that point. For example:

>>> def sample(n):
...     if n > 0:
...             sample(n-1)
...     else:
...             traceback.print_stack(file=sys.stderr)
...
>>> sample(5)
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in sample
  File "<stdin>", line 3, in sample
  File "<stdin>", line 3, in sample
  File "<stdin>", line 3, in sample
  File "<stdin>", line 3, in sample
  File "<stdin>", line 5, in sample
>>>

Alternatively, you can also manually launch the debugger at any point in your program
using pdb.set_trace() like this:

import pdb

def func(arg):
    ...
    pdb.set_trace()
    ...

This can be a useful technique for poking around in the internals of a large program
and answering questions about the control flow or arguments to functions. For instance,
once the debugger starts, you can inspect variables using print or type a command such
as w to get the stack traceback.

|

----------
讨论
----------
Don’t make debugging more complicated than it needs to be. Simple errors can often
be resolved by merely knowing how to read program tracebacks (e.g., the actual error
is usually the last line of the traceback). Inserting a few selected print() functions in
your code can also work well if you’re in the process of developing it and you simply
want some diagnostics (just remember to remove the statements later).
A common use of the debugger is to inspect variables inside a function that has crashed.
Knowing how to enter the debugger after such a crash has occurred is a useful skill to
know.
Inserting statements such as pdb.set_trace() can be useful if you’re trying to unravel
an extremely complicated program where the underlying control flow isn’t obvious.
Essentially, the program will run until it hits the set_trace() call, at which point it will
immediately enter the debugger. From there, you can try to make more sense of it. 
If you’re using an IDE for Python development, the IDE will typically provide its own
debugging interface on top of or in place of pdb. Consult the manual for your IDE for
more information.
