==============================
13.13 记录程序执行的时间
==============================

----------
问题
----------
You want to be able to record the time it takes to perform various tasks.

Solution
The time module contains various functions for performing timing-related functions.
However, it’s often useful to put a higher-level interface on them that mimics a stop
watch. For example:

import time

class Timer:
    def __init__(self, func=time.perf_counter):
        self.elapsed = 0.0
        self._func = func
        self._start = None

    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = self._func()

    def stop(self):
        if self._start is None:
            raise RuntimeError('Not started')
        end = self._func()
        self.elapsed += end - self._start
        self._start = None

    def reset(self):
        self.elapsed = 0.0

    @property
    def running(self):
        return self._start is not None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

This class defines a timer that can be started, stopped, and reset as needed by the user.
It keeps track of the total elapsed time in the elapsed attribute. Here is an example that
shows how it can be used:

def countdown(n):
    while n > 0:
        n -= 1

# Use 1: Explicit start/stop
t = Timer()
t.start()
countdown(1000000)
t.stop()
print(t.elapsed)

# Use 2: As a context manager
with t:
    countdown(1000000)

print(t.elapsed)

with Timer() as t2:
    countdown(1000000)
print(t2.elapsed)

Discussion
This recipe provides a simple yet very useful class for making timing measurements and
tracking  elapsed  time.  It’s  also  a  nice  illustration  of  how  to  support  the  context-
management protocol and the with statement.
One issue in making timing measurements concerns the underlying time function used
to do it. As a general rule, the accuracy of timing measurements made with functions
such as  time.time() or  time.clock() varies according to the operating system. In
contrast, the time.perf_counter() function always uses the highest-resolution timer
available on the system.
As shown, the time recorded by the Timer class is made according to wall-clock time,
and includes all time spent sleeping. If you only want the amount of CPU time used by
the process, use time.process_time() instead. For example:

t = Timer(time.process_time)
with t:
    countdown(1000000)
print(t.elapsed)

Both the time.perf_counter() and time.process_time() return a “time” in fractional
seconds. However, the actual value of the time doesn’t have any particular meaning. To
make sense of the results, you have to call the functions twice and compute a time
difference.
More examples of timing and profiling are given in Recipe 14.13.
