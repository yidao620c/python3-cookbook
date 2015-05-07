==============================
15.21 诊断分析代码错误
==============================

----------
问题
----------
The interpreter violently crashes with a segmentation fault, bus error, access violation,
or other fatal error. You would like to get a Python traceback that shows you where your
program was running at the point of failure.

Solution
The  faulthandler module can be used to help you solve this problem. Include the
following code in your program:

import faulthandler
faulthandler.enable()

Alternatively, run Python with the -Xfaulthandler option such as this:

bash % python3 -Xfaulthandler program.py

Last, but not least, you can set the PYTHONFAULTHANDLER environment variable.
With faulthandler enabled, fatal errors in C extensions will result in a Python trace‐
back being printed on failures. For example:

    Fatal Python error: Segmentation fault

    Current thread 0x00007fff71106cc0:
      File "example.py", line 6 in foo
      File "example.py", line 10 in bar
      File "example.py", line 14 in spam
      File "example.py", line 19 in <module>
    Segmentation fault

Although this won’t tell you where in the C code things went awry, at least it can tell you
how it got there from Python.

Discussion
The faulthandler will show you the stack traceback of the Python code executing at
the time of failure. At the very least, this will show you the top-level extension function
that was invoked. With the aid of pdb or other Python debugger, you can investigate the
flow of the Python code leading to the error.
faulthandler will not tell you anything about the failure from C. For that, you will
need to use a traditional C debugger, such as gdb. However, the information from the
faulthandler traceback may give you a better idea of where to direct your attention.
It should be noted that certain kinds of errors in C may not be easily recoverable. For
example, if a C extension trashes the stack or program heap, it may render faulthan
dler inoperable and you’ll simply get no output at all (other than a crash). Obviously,
your mileage may vary.

