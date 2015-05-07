==============================
13.14 限制内存和CPU的使用量
==============================

----------
问题
----------
You want to place some limits on the memory or CPU use of a program running on
Unix system.

|

----------
解决方案
----------
The resource module can be used to perform both tasks. For example, to restrict CPU
time, do the following:

import signal
import resource
import os

def time_exceeded(signo, frame):
    print("Time's up!")
    raise SystemExit(1)

def set_max_runtime(seconds):
    # Install the signal handler and set a resource limit
    soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
    resource.setrlimit(resource.RLIMIT_CPU, (seconds, hard))
    signal.signal(signal.SIGXCPU, time_exceeded)

if __name__ == '__main__':
    set_max_runtime(15)
    while True:
        pass

When this runs, the SIGXCPU signal is generated when the time expires. The program
can then clean up and exit.
To restrict memory use, put a limit on the total address space in use. For example:

import resource

def limit_memory(maxsize):
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (maxsize, hard))

With a memory limit in place, programs will start generating MemoryError exceptions
when no more memory is available.

|

----------
讨论
----------
In this recipe, the setrlimit() function is used to set a soft and hard limit on a particular
resource. The soft limit is a value upon which the operating system will typically restrict
or notify the process via a signal. The hard limit represents an upper bound on the values
that may be used for the soft limit. Typically, this is controlled by a system-wide pa‐
rameter set by the system administrator. Although the hard limit can be lowered, it can
never be raised by user processes (even if the process lowered itself).
The setrlimit() function can additionally be used to set limits on things such as the
number of child processes, number of open files, and similar system resources. Consult
the documentation for the resource module for further details.
Be aware that this recipe only works on Unix systems, and that it might not work on all
of them. For example, when tested, it works on Linux but not on OS X.

