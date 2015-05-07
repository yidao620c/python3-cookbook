============================
12.4 给关键部分加锁
============================

----------
问题
----------
Your program uses threads and you want to lock critical sections of code to avoid race
conditions.

Solution
To make mutable objects safe to use by multiple threads, use Lock objects in the thread
ing library, as shown here:

import threading

class SharedCounter:
    '''
    A counter object that can be shared by multiple threads.
    '''
    def __init__(self, initial_value = 0):
        self._value = initial_value
        self._value_lock = threading.Lock()

    def incr(self,delta=1):
        '''
        Increment the counter with locking
        '''
        with self._value_lock:
             self._value += delta

    def decr(self,delta=1):
        '''
        Decrement the counter with locking
        '''
        with self._value_lock:
             self._value -= delta

A Lock guarantees mutual exclusion when used with the with statement—that is, only
one thread is allowed to execute the block of statements under the with statement at a
time. The with statement acquires the lock for the duration of the indented statements
and releases the lock when control flow exits the indented block.

Discussion
Thread scheduling is inherently nondeterministic. Because of this, failure to use locks
in  threaded  programs  can  result  in  randomly  corrupted  data  and  bizarre  behavior
known as a “race condition.” To avoid this, locks should always be used whenever shared
mutable state is accessed by multiple threads.

In older Python code, it is common to see locks explicitly acquired and released. For
example, in this variant of the last example:

import threading

class SharedCounter:
    '''
    A counter object that can be shared by multiple threads.
    '''
    def __init__(self, initial_value = 0):
        self._value = initial_value
        self._value_lock = threading.Lock()

    def incr(self,delta=1):
        '''
        Increment the counter with locking
        '''
        self._value_lock.acquire()
        self._value += delta
        self._value_lock.release()

    def decr(self,delta=1):
        '''
        Decrement the counter with locking
        '''
        self._value_lock.acquire()
        self._value -= delta
        self._value_lock.release()

The with statement is more elegant and less prone to error—especially in situations
where a programmer might forget to call the release() method or if a program happens
to raise an exception while holding a lock (the with statement guarantees that locks are
always released in both cases).
To avoid the potential for deadlock, programs that use locks should be written in a way
such that each thread is only allowed to acquire one lock at a time. If this is not possible,
you may need to introduce more advanced deadlock avoidance into your program, as
described in Recipe 12.5.
In the threading library, you’ll find other synchronization primitives, such as RLock
and Semaphore objects. As a general rule of thumb, these are more special purpose and
should not be used for simple locking of mutable state. An RLock or re-entrant lock
object is a lock that can be acquired multiple times by the same thread. It is primarily
used to implement code based locking or synchronization based on a construct known
as a “monitor.” With this kind of locking, only one thread is allowed to use an entire
function or the methods of a class while the lock is held. For example, you could im‐
plement the SharedCounter class like this:

import threading

class SharedCounter:
    '''
    A counter object that can be shared by multiple threads.
    '''
    _lock = threading.RLock()
    def __init__(self, initial_value = 0):
        self._value = initial_value

    def incr(self,delta=1):
        '''
        Increment the counter with locking
        '''
        with SharedCounter._lock:
            self._value += delta

    def decr(self,delta=1):
        '''
        Decrement the counter with locking
        '''
        with SharedCounter._lock:
             self.incr(-delta)

In this variant of the code, there is just a single class-level lock shared by all instances
of the class. Instead of the lock being tied to the per-instance mutable state, the lock is
meant to synchronize the methods of the class. Specifically, this lock ensures that only
one thread is allowed to be using the methods of the class at once. However, unlike a
standard lock, it is OK for methods that already have the lock to call other methods that
also use the lock (e.g., see the decr() method).
One feature of this implementation is that only one lock is created, regardless of how
many counter instances are created. Thus, it is much more memory-efficient in situa‐
tions where there are a large number of counters. However, a possible downside is that
it may cause more lock contention in programs that use a large number of threads and
make frequent counter updates.
A Semaphore object is a synchronization primitive based on a shared counter. If the
counter is nonzero, the with statement decrements the count and a thread is allowed to
proceed. The counter is incremented upon the conclusion of the  with block. If the
counter is zero, progress is blocked until the counter is incremented by another thread.
Although a semaphore can be used in the same manner as a standard Lock, the added
complexity in implementation negatively impacts performance. Instead of simple lock‐
ing, Semaphore objects are more useful for applications involving signaling between
threads or throttling. For example, if you want to limit the amount of concurrency in a
part of code, you might use a semaphore, as follows:

from threading import Semaphore
import urllib.request

# At most, five threads allowed to run at once
_fetch_url_sema = Semaphore(5)

def fetch_url(url):
    with _fetch_url_sema:
        return urllib.request.urlopen(url)

If you’re interested in the underlying theory and implementation of thread synchroni‐
zation primitives, consult almost any textbook on operating systems.
