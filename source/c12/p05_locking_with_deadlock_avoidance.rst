============================
12.5 防止死锁的加锁机制
============================

----------
问题
----------
You’re writing a multithreaded program where threads need to acquire more than one
lock at a time while avoiding deadlock.

Solution
In multithreaded programs, a common source of deadlock is due to threads that attempt
to acquire multiple locks at once. For instance, if a thread acquires the first lock, but
then blocks trying to acquire the second lock, that thread can potentially block the
progress of other threads and make the program freeze.
One solution to deadlock avoidance is to assign each lock in the program a unique
number, and to enforce an ordering rule that only allows multiple locks to be acquired
in ascending order. This is surprisingly easy to implement using a context manager as
follows:

import threading
from contextlib import contextmanager

# Thread-local state to stored information on locks already acquired
_local = threading.local()

@contextmanager
def acquire(*locks):
    # Sort locks by object identifier
    locks = sorted(locks, key=lambda x: id(x))

    # Make sure lock order of previously acquired locks is not violated
    acquired = getattr(_local,'acquired',[])
    if acquired and max(id(lock) for lock in acquired) >= id(locks[0]):
        raise RuntimeError('Lock Order Violation')

    # Acquire all of the locks
    acquired.extend(locks)
    _local.acquired = acquired

    try:
        for lock in locks:
            lock.acquire()
        yield
    finally:
        # Release locks in reverse order of acquisition
        for lock in reversed(locks):
            lock.release()
        del acquired[-len(locks):]

To use this context manager, you simply allocate lock objects in the normal way, but use
the  acquire()  function  whenever  you  want  to  work  with  one  or  more  locks.  For
example:

import threading
x_lock = threading.Lock()
y_lock = threading.Lock()

def thread_1():
    while True:
        with acquire(x_lock, y_lock):
            print('Thread-1')

def thread_2():
    while True:
        with acquire(y_lock, x_lock):
            print('Thread-2')

t1 = threading.Thread(target=thread_1)
t1.daemon = True
t1.start()

t2 = threading.Thread(target=thread_2)
t2.daemon = True
t2.start()

If you run this program, you’ll find that it happily runs forever without deadlock—even
though the acquisition of locks is specified in a different order in each function.
The key to this recipe lies in the first statement that sorts the locks according to object
identifier. By sorting the locks, they always get acquired in a consistent order regardless
of how the user might have provided them to acquire().
The solution uses thread-local storage to solve a subtle problem with detecting potential
deadlock if multiple acquire() operations are nested. For example, suppose you wrote
the code like this:

import threading
x_lock = threading.Lock()
y_lock = threading.Lock()

def thread_1():

    while True:
        with acquire(x_lock):
            with acquire(y_lock):
                print('Thread-1')

def thread_2():
    while True:
        with acquire(y_lock):
            with acquire(x_lock):
                print('Thread-2')

t1 = threading.Thread(target=thread_1)
t1.daemon = True
t1.start()

t2 = threading.Thread(target=thread_2)
t2.daemon = True
t2.start()

If you run this version of the program, one of the threads will crash with an exception
such as this:

Exception in thread Thread-1:
Traceback (most recent call last):
  File "/usr/local/lib/python3.3/threading.py", line 639, in _bootstrap_inner
    self.run()
  File "/usr/local/lib/python3.3/threading.py", line 596, in run
    self._target(*self._args, **self._kwargs)
  File "deadlock.py", line 49, in thread_1
    with acquire(y_lock):
  File "/usr/local/lib/python3.3/contextlib.py", line 48, in __enter__
    return next(self.gen)
  File "deadlock.py", line 15, in acquire
    raise RuntimeError("Lock Order Violation")
RuntimeError: Lock Order Violation
>>>

This crash is caused by the fact that each thread remembers the locks it has already
acquired. The acquire() function checks the list of previously acquired locks and en‐
forces the ordering constraint that previously acquired locks must have an object ID
that is less than the new locks being acquired.

Discussion
The issue of deadlock is a well-known problem with programs involving threads (as
well as a common subject in textbooks on operating systems). As a rule of thumb, as
long as you can ensure that threads can hold only one lock at a time, your program will
be deadlock free. However, once multiple locks are being acquired at the same time, all
bets are off.

Detecting and recovering from deadlock is an extremely tricky problem with few elegant
solutions. For example, a common deadlock detection and recovery scheme involves
the use of a watchdog timer. As threads run, they periodically reset the timer, and as
long as everything is running smoothly, all is well. However, if the program deadlocks,
the watchdog timer will eventually expire. At that point, the program “recovers” by
killing and then restarting itself.
Deadlock avoidance is a different strategy where locking operations are carried out in
a manner that simply does not allow the program to enter a deadlocked state. The
solution in which locks are always acquired in strict order of ascending object ID can
be mathematically proven to avoid deadlock, although the proof is left as an exercise to
the reader (the gist of it is that by acquiring locks in a purely increasing order, you can’t
get cyclic locking dependencies, which are a necessary condition for deadlock to occur).
As a final example, a classic thread deadlock problem is the so-called “dining philoso‐
pher’s problem.” In this problem, five philosophers sit around a table on which there
are five bowls of rice and five chopsticks. Each philosopher represents an independent
thread and each chopstick represents a lock. In the problem, philosophers either sit and
think or they eat rice. However, in order to eat rice, a philosopher needs two chopsticks.
Unfortunately, if all of the philosophers reach over and grab the chopstick to their left,
they’ll all just sit there with one stick and eventually starve to death. It’s a gruesome
scene.
Using the solution, here is a simple deadlock free implementation of the dining philos‐
opher’s problem:

import threading

# The philosopher thread
def philosopher(left, right):
    while True:
        with acquire(left,right):
             print(threading.currentThread(), 'eating')

# The chopsticks (represented by locks)
NSTICKS = 5
chopsticks = [threading.Lock() for n in range(NSTICKS)]

# Create all of the philosophers
for n in range(NSTICKS):
    t = threading.Thread(target=philosopher,
                         args=(chopsticks[n],chopsticks[(n+1) % NSTICKS]))
    t.start()

Last, but not least, it should be noted that in order to avoid deadlock, all locking oper‐
ations must be carried out using our acquire() function. If some fragment of code
decided to acquire a lock directly, then the deadlock avoidance algorithm wouldn’t work.

