============================
12.8 简单的并行编程
============================

----------
问题
----------
You have a program that performs a lot of CPU-intensive work, and you want to make
it run faster by having it take advantage of multiple CPUs.

|

----------
解决方案
----------
The concurrent.futures library provides a ProcessPoolExecutor class that can be
used to execute computationally intensive functions in a separately running instance of
the Python interpreter. However, in order to use it, you first need to have some com‐
putationally intensive work. Let’s illustrate with a simple yet practical example.
Suppose you have an entire directory of gzip-compressed Apache web server logs:

logs/
   20120701.log.gz
   20120702.log.gz
   20120703.log.gz
   20120704.log.gz
   20120705.log.gz
   20120706.log.gz
   ...

Further suppose each log file contains lines like this:

124.115.6.12 - - [10/Jul/2012:00:18:50 -0500] "GET /robots.txt ..." 200 71
210.212.209.67 - - [10/Jul/2012:00:18:51 -0500] "GET /ply/ ..." 200 11875
210.212.209.67 - - [10/Jul/2012:00:18:51 -0500] "GET /favicon.ico ..." 404 369
61.135.216.105 - - [10/Jul/2012:00:20:04 -0500] "GET /blog/atom.xml ..." 304 -
...

Here is a simple script that takes this data and identifies all hosts that have accessed the
robots.txt file:

# findrobots.py

import gzip
import io
import glob

def find_robots(filename):
    '''
    Find all of the hosts that access robots.txt in a single log file
    '''
    robots = set()
    with gzip.open(filename) as f:
        for line in io.TextIOWrapper(f,encoding='ascii'):
            fields = line.split()
            if fields[6] == '/robots.txt':
                robots.add(fields[0])
    return robots

def find_all_robots(logdir):
    '''
    Find all hosts across and entire sequence of files
    '''
    files = glob.glob(logdir+'/*.log.gz')
    all_robots = set()
    for robots in map(find_robots, files):
        all_robots.update(robots)
    return all_robots

if __name__ == '__main__':
    robots = find_all_robots('logs')
    for ipaddr in robots:
        print(ipaddr)

The preceding program is written in the commonly used map-reduce style. The function
find_robots() is mapped across a collection of filenames and the results are combined
into a single result (the all_robots set in the find_all_robots() function).
Now, suppose you want to modify this program to use multiple CPUs. It turns out to
be easy—simply replace the map() operation with a similar operation carried out on a
process pool from the concurrent.futures library. Here is a slightly modified version
of the code:

# findrobots.py

import gzip
import io
import glob
from concurrent import futures

def find_robots(filename):
    '''
    Find all of the hosts that access robots.txt in a single log file

    '''
    robots = set()
    with gzip.open(filename) as f:
        for line in io.TextIOWrapper(f,encoding='ascii'):
            fields = line.split()
            if fields[6] == '/robots.txt':
                robots.add(fields[0])
    return robots

def find_all_robots(logdir):
    '''
    Find all hosts across and entire sequence of files
    '''
    files = glob.glob(logdir+'/*.log.gz')
    all_robots = set()
    with futures.ProcessPoolExecutor() as pool:
        for robots in pool.map(find_robots, files):
            all_robots.update(robots)
    return all_robots

if __name__ == '__main__':
    robots = find_all_robots('logs')
    for ipaddr in robots:
        print(ipaddr)

With this modification, the script produces the same result but runs about 3.5 times
faster on our quad-core machine. The actual performance will vary according to the
number of CPUs available on your machine.

|

----------
讨论
----------
Typical usage of a ProcessPoolExecutor is as follows:
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor() as pool:
    ...
    do work in parallel using pool
    ...

Under the covers, a ProcessPoolExecutor creates N independent running Python in‐
terpreters where N is the number of available CPUs detected on the system. You can
change the number of processes created by supplying an optional argument to Proces
sPoolExecutor(N). The pool runs until the last statement in the with block is executed,
at which point the process pool is shut down. However, the program will wait until all
submitted work has been processed.
Work to be submitted to a pool must be defined in a function. There are two methods
for submission. If you are are trying to parallelize a list comprehension or a  map()
operation, you use pool.map():

# A function that performs a lot of work
def work(x):
    ...
    return result

# Nonparallel code
results = map(work, data)

# Parallel implementation
with ProcessPoolExecutor() as pool:
    results = pool.map(work, data)

Alternatively, you can manually submit single tasks using the pool.submit() method:

# Some function
def work(x):
    ...
    return result

with ProcessPoolExecutor() as pool:
    ...
    # Example of submitting work to the pool
    future_result = pool.submit(work, arg)

    # Obtaining the result (blocks until done)
    r = future_result.result()
    ...

If you manually submit a job, the result is an instance of Future. To obtain the actual
result, you call its result() method. This blocks until the result is computed and re‐
turned by the pool.
Instead of blocking, you can also arrange to have a callback function triggered upon
completion instead. For example:

def when_done(r):
    print('Got:', r.result())

with ProcessPoolExecutor() as pool:
     future_result = pool.submit(work, arg)
     future_result.add_done_callback(when_done)

The user-supplied callback function receives an instance of Future that must be used
to obtain the actual result (i.e., by calling its result() method).
Although process pools can be easy to use, there are a number of important consider‐
ations to be made in designing larger programs. In no particular order:

• This technique for parallelization only works well for problems that can be trivially

decomposed into independent parts.

• Work must be submitted in the form of simple functions. Parallel execution of

instance methods, closures, or other kinds of constructs are not supported.

• Function arguments and return values must be compatible with pickle. Work is
carried out in a separate interpreter using interprocess communication. Thus, data
exchanged between interpreters has to be serialized.

• Functions submitted for work should not maintain persistent state or have side
effects. With the exception of simple things such as logging, you don’t really have
any control over the behavior of child processes once started. Thus, to preserve your
sanity, it is probably best to keep things simple and carry out work in pure-functions
that don’t alter their environment.

• Process pools are created by calling the fork() system call on Unix. This makes a
clone of the Python interpreter, including all of the program state at the time of the
fork. On Windows, an independent copy of the interpreter that does not clone state
is launched. The actual forking process does not occur until the first pool.map()
or pool.submit() method is called.

• Great care should be made when combining process pools and programs that use
threads. In particular, you should probably create and launch process pools prior
to the creation of any threads (e.g., create the pool in the main thread at program
startup).

