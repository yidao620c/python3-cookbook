============================
12.1 启动与停止线程
============================

----------
问题
----------
You want to create and destroy threads for concurrent execution of code.

|

----------
解决方案
----------
The threading library can be used to execute any Python callable in its own thread. To
do this, you create a Thread instance and supply the callable that you wish to execute
as a target. Here is a simple example:

# Code to execute in an independent thread
import time
def countdown(n):
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(5)

# Create and launch a thread
from threading import Thread
t = Thread(target=countdown, args=(10,))
t.start()

When you create a thread instance, it doesn’t start executing until you invoke its start()
method (which invokes the target function with the arguments you supplied).
Threads are executed in their own system-level thread (e.g., a POSIX thread or Windows
threads) that is fully managed by the host operating system. Once started, threads run
independently until the target function returns. You can query a thread instance to see
if it’s still running:

if t.is_alive():
    print('Still running')
else:
    print('Completed')

You can also request to join with a thread, which waits for it to terminate:

    t.join()

The interpreter remains running until all threads terminate. For long-running threads
or background tasks that run forever, you should consider making the thread daemonic.
For example:

t = Thread(target=countdown, args=(10,), daemon=True)
t.start()

Daemonic threads can’t be joined. However, they are destroyed automatically when the
main thread terminates.
Beyond the two operations shown, there aren’t many other things you can do with
threads. For example, there are no operations to terminate a thread, signal a thread,
adjust its scheduling, or perform any other high-level operations. If you want these
features, you need to build them yourself.
If you want to be able to terminate threads, the thread must be programmed to poll for
exit at selected points. For example, you might put your thread in a class such as this:

class CountdownTask:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, n):
        while self._running and n > 0:
            print('T-minus', n)
            n -= 1
            time.sleep(5)

c = CountdownTask()
t = Thread(target=c.run, args=(10,))
t.start()
...
c.terminate() # Signal termination
t.join()      # Wait for actual termination (if needed)

Polling for thread termination can be tricky to coordinate if threads perform blocking
operations such as I/O. For example, a thread blocked indefinitely on an I/O operation
may never return to check if it’s been killed. To correctly deal with this case, you’ll need
to carefully program thread to utilize timeout loops. For example:

class IOTask:
    def terminate(self):
        self._running = False

    def run(self, sock):
        # sock is a socket
        sock.settimeout(5)        # Set timeout period
        while self._running:
            # Perform a blocking I/O operation w/ timeout
            try:
                data = sock.recv(8192)
                break
            except socket.timeout:
                continue
            # Continued processing
            ...
        # Terminated
        return

|

----------
讨论
----------
Due to a global interpreter lock (GIL), Python threads are restricted to an execution
model that only allows one thread to execute in the interpreter at any given time. For
this reason, Python threads should generally not be used for computationally intensive
tasks where you are trying to achieve parallelism on multiple CPUs. They are much
better suited for I/O handling and handling concurrent execution in code that performs
blocking operations (e.g., waiting for I/O, waiting for results from a database, etc.).
Sometimes  you  will  see  threads  defined  via  inheritance  from  the  Thread  class.  For
example:

from threading import Thread

class CountdownThread(Thread):
    def __init__(self, n):
        super().__init__()
        self.n = 0
    def run(self):
        while self.n > 0:

            print('T-minus', self.n)
            self.n -= 1
            time.sleep(5)

c = CountdownThread(5)
c.start()

Although this works, it introduces an extra dependency between the code and the 
threading library. That is, you can only use the resulting code in the context of threads,
whereas the technique shown earlier involves writing code with no explicit dependency
on threading. By freeing your code of such dependencies, it becomes usable in other
contexts that may or may not involve threads. For instance, you might be able to execute
your code in a separate process using the multiprocessing module using code like this:

import multiprocessing
c = CountdownTask(5)
p = multiprocessing.Process(target=c.run)
p.start()
...

Again, this only works if the CountdownTask class has been written in a manner that is
neutral to the actual means of concurrency (threads, processes, etc.).
