==============================
14.13 给你的程序做基准测试
==============================

----------
问题
----------
You  would  like  to  find  out  where  your  program  spends  its  time  and  make  timing
measurements.

Solution
If you simply want to time your whole program, it’s usually easy enough to use something
like the Unix time command. For example:

bash % time python3 someprogram.py
real 0m13.937s
user 0m12.162s
sys  0m0.098s
bash %

On the other extreme, if you want a detailed report showing what your program is doing,
you can use the cProfile module:

bash % python3 -m cProfile someprogram.py
         859647 function calls in 16.016 CPU seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   263169    0.080    0.000    0.080    0.000 someprogram.py:16(frange)
      513    0.001    0.000    0.002    0.000 someprogram.py:30(generate_mandel)
   262656    0.194    0.000   15.295    0.000 someprogram.py:32(<genexpr>)
        1    0.036    0.036   16.077   16.077 someprogram.py:4(<module>)
   262144   15.021    0.000   15.021    0.000 someprogram.py:4(in_mandelbrot)
        1    0.000    0.000    0.000    0.000 os.py:746(urandom)
        1    0.000    0.000    0.000    0.000 png.py:1056(_readable)
        1    0.000    0.000    0.000    0.000 png.py:1073(Reader)
        1    0.227    0.227    0.438    0.438 png.py:163(<module>)
      512    0.010    0.000    0.010    0.000 png.py:200(group)
    ...
bash %

More often than not, profiling your code lies somewhere in between these two extremes.
For example, you may already know that your code spends most of its time in a few
selected functions. For selected profiling of functions, a short decorator can be useful.
For example:

# timethis.py

import time
from functools import wraps

def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print('{}.{} : {}'.format(func.__module__, func.__name__, end - start))
        return r
    return wrapper

To use this decorator, you simply place it in front of a function definition to get timings
from it. For example:

>>> @timethis
... def countdown(n):
...     while n > 0:
...             n -= 1
...
>>> countdown(10000000)
__main__.countdown : 0.803001880645752
>>>

To time a block of statements, you can define a context manager. For example:

from contextlib import contextmanager

@contextmanager
def timeblock(label):
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print('{} : {}'.format(label, end - start))
Here is an example of how the context manager works:

>>> with timeblock('counting'):
...     n = 10000000
...     while n > 0:
...             n -= 1
...
counting : 1.5551159381866455
>>>

For studying the performance of small code fragments, the timeit module can be useful.
For example:

>>> from timeit import timeit
>>> timeit('math.sqrt(2)', 'import math')
0.1432319980012835
>>> timeit('sqrt(2)', 'from math import sqrt')
0.10836604500218527
>>>

timeit works by executing the statement specified in the first argument a million times
and measuring the time. The second argument is a setup string that is executed to set
up the environment prior to running the test. If you need to change the number of
iterations, supply a number argument like this:

>>> timeit('math.sqrt(2)', 'import math', number=10000000)
1.434852126003534
>>> timeit('sqrt(2)', 'from math import sqrt', number=10000000)
1.0270336690009572
>>>

Discussion
When making performance measurements, be aware that any results you get are ap‐
proximations. The time.perf_counter() function used in the solution provides the
highest-resolution timer possible on a given platform. However, it still measures wall-
clock time, and can be impacted by many different factors, such as machine load.
If  you  are  interested  in  process  time  as  opposed  to  wall-clock  time,  use  time.pro
cess_time() instead. For example:

from functools import wraps
def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.process_time()
        r = func(*args, **kwargs)
        end = time.process_time()
        print('{}.{} : {}'.format(func.__module__, func.__name__, end - start))
        return r
    return wrapper

Last, but not least, if you’re going to perform detailed timing analysis, make sure to read
the documentation for the time, timeit, and other associated modules, so that you have
an understanding of important platform-related differences and other pitfalls.
See Recipe 13.13 for a related recipe on creating a stopwatch timer class.
