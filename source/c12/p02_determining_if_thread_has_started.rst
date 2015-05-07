============================
12.2 判断线程是否已经启动
============================

----------
问题
----------
You’ve launched a thread, but want to know when it actually starts running.

Solution
A key feature of threads is that they execute independently and nondeterministically.
This can present a tricky synchronization problem if other threads in the program need
to know if a thread has reached a certain point in its execution before carrying out
further operations. To solve such problems, use the Event object from the threading
library.
Event instances are similar to a “sticky” flag that allows threads to wait for something
to happen. Initially, an event is set to 0. If the event is unset and a thread waits on the
event, it will block (i.e., go to sleep) until the event gets set. A thread that sets the event
will wake up all of the threads that happen to be waiting (if any). If a thread waits on an
event that has already been set, it merely moves on, continuing to execute.
Here is some sample code that uses an Event to coordinate the startup of a thread:

from threading import Thread, Event
import time

# Code to execute in an independent thread
def countdown(n, started_evt):
    print('countdown starting')
    started_evt.set()
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(5)

# Create the event object that will be used to signal startup
started_evt = Event()

# Launch the thread and pass the startup event
print('Launching countdown')
t = Thread(target=countdown, args=(10,started_evt))
t.start()

# Wait for the thread to start
started_evt.wait()
print('countdown is running')

When you run this code, the “countdown is running” message will always appear after
the “countdown starting” message. This is coordinated by the event that makes the main
thread wait until the countdown() function has first printed the startup message.

Discussion
Event objects are best used for one-time events. That is, you create an event, threads
wait for the event to be set, and once set, the Event is discarded. Although it is possible
to clear an event using its clear() method, safely clearing an event and waiting for it
to be set again is tricky to coordinate, and can lead to missed events, deadlock, or other
problems (in particular, you can’t guarantee that a request to clear an event after setting
it will execute before a released thread cycles back to wait on the event again).
If a thread is going to repeatedly signal an event over and over, you’re probably better
off using a Condition object instead. For example, this code implements a periodic timer
that other threads can monitor to see whenever the timer expires:

import threading
import time

class PeriodicTimer:
    def __init__(self, interval):
        self._interval = interval
        self._flag = 0
        self._cv = threading.Condition()

    def start(self):
        t = threading.Thread(target=self.run)
        t.daemon = True

        t.start()

    def run(self):
        '''
        Run the timer and notify waiting threads after each interval
        '''
        while True:
            time.sleep(self._interval)
            with self._cv:
                 self._flag ^= 1
                 self._cv.notify_all()

    def wait_for_tick(self):
        '''
        Wait for the next tick of the timer
        '''
        with self._cv:
            last_flag = self._flag
            while last_flag == self._flag:
                self._cv.wait()

# Example use of the timer
ptimer = PeriodicTimer(5)
ptimer.start()

# Two threads that synchronize on the timer
def countdown(nticks):
    while nticks > 0:
        ptimer.wait_for_tick()
        print('T-minus', nticks)
        nticks -= 1

def countup(last):
    n = 0
    while n < last:
        ptimer.wait_for_tick()
        print('Counting', n)
        n += 1

threading.Thread(target=countdown, args=(10,)).start()
threading.Thread(target=countup, args=(5,)).start()

A critical feature of Event objects is that they wake all waiting threads. If you are writing
a program where you only want to wake up a single waiting thread, it is probably better
to use a Semaphore or Condition object instead.
For example, consider this code involving semaphores:

# Worker thread
def worker(n, sema):
    # Wait to be signaled
    sema.acquire()

    # Do some work
    print('Working', n)

# Create some threads
sema = threading.Semaphore(0)
nworkers = 10
for n in range(nworkers):
    t = threading.Thread(target=worker, args=(n, sema,))
    t.start()

If you run this, a pool of threads will start, but nothing happens because they’re all
blocked waiting to acquire the semaphore. Each time the semaphore is released, only
one worker will wake up and run. For example:

>>> sema.release()
Working 0
>>> sema.release()
Working 1
>>>

Writing code that involves a lot of tricky synchronization between threads is likely to
make your head explode. A more sane approach is to thread threads as communicating
tasks using queues or as actors. Queues are described in the next recipe. Actors are
described in Recipe 12.10.
