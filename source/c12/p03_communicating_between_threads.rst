============================
12.3 线程间的通信
============================

----------
问题
----------
You have multiple threads in your program and you want to safely communicate or
exchange data between them.

Solution
Perhaps the safest way to send data from one thread to another is to use a Queue from
the queue library. To do this, you create a Queue instance that is shared by the threads.
Threads then use put() or get() operations to add or remove items from the queue.
For example:

from queue import Queue
from threading import Thread

# A thread that produces data
def producer(out_q):
    while True:
        # Produce some data
        ...
        out_q.put(data)

# A thread that consumes data
def consumer(in_q):
    while True:
        # Get some data
        data = in_q.get()
        # Process the data
        ...

# Create the shared queue and launch both threads
q = Queue()
t1 = Thread(target=consumer, args=(q,))
t2 = Thread(target=producer, args=(q,))
t1.start()
t2.start()

Queue instances already have all of the required locking, so they can be safely shared by
as many threads as you wish.
When using queues, it can be somewhat tricky to coordinate the shutdown of the pro‐
ducer and consumer. A common solution to this problem is to rely on a special sentinel
value, which when placed in the queue, causes consumers to terminate. For example:

from queue import Queue
from threading import Thread

# Object that signals shutdown
_sentinel = object()

# A thread that produces data
def producer(out_q):
    while running:
        # Produce some data
        ...
        out_q.put(data)

    # Put the sentinel on the queue to indicate completion
    out_q.put(_sentinel)

# A thread that consumes data
def consumer(in_q):
    while True:
        # Get some data
        data = in_q.get()

        # Check for termination
        if data is _sentinel:
            in_q.put(_sentinel)
            break

        # Process the data
        ...

A subtle feature of this example is that the consumer, upon receiving the special sentinel
value, immediately places it back onto the queue. This propagates the sentinel to other
consumers threads that might be listening on the same queue—thus shutting them all
down one after the other.
Although queues are the most common thread communication mechanism, you can
build your own data structures as long as you add the required locking and synchroni‐
zation. The most common way to do this is to wrap your data structures with a condition
variable. For example, here is how you might build a thread-safe priority queue, as
discussed in Recipe 1.5.

import heapq
import threading

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._count = 0
        self._cv = threading.Condition()
    def put(self, item, priority):
        with self._cv:
            heapq.heappush(self._queue, (-priority, self._count, item))
            self._count += 1
            self._cv.notify()

    def get(self):
        with self._cv:
            while len(self._queue) == 0:
                self._cv.wait()
            return heapq.heappop(self._queue)[-1]

Thread communication with a queue is a one-way and nondeterministic process. In
general, there is no way to know when the receiving thread has actually received a
message and worked on it. However, Queue objects do provide some basic completion
features, as illustrated by the task_done() and join() methods in this example:

from queue import Queue
from threading import Thread

# A thread that produces data
def producer(out_q):
    while running:
        # Produce some data
        ...
        out_q.put(data)

# A thread that consumes data
def consumer(in_q):
    while True:
        # Get some data
        data = in_q.get()

        # Process the data
        ...
        # Indicate completion
        in_q.task_done()

# Create the shared queue and launch both threads
q = Queue()
t1 = Thread(target=consumer, args=(q,))
t2 = Thread(target=producer, args=(q,))
t1.start()
t2.start()

# Wait for all produced items to be consumed
q.join()

If a thread needs to know immediately when a consumer thread has processed a par‐
ticular item of data, you should pair the sent data with an Event object that allows the
producer to monitor its progress. For example:

from queue import Queue
from threading import Thread, Event

# A thread that produces data
def producer(out_q):
    while running:
        # Produce some data
        ...
        # Make an (data, event) pair and hand it to the consumer
        evt = Event()
        out_q.put((data, evt))
        ...
        # Wait for the consumer to process the item
        evt.wait()

# A thread that consumes data
def consumer(in_q):
    while True:
        # Get some data
        data, evt = in_q.get()
        # Process the data
        ...
        # Indicate completion
        evt.set()

Discussion
Writing threaded programs based on simple queuing is often a good way to maintain
sanity. If you can break everything down to simple thread-safe queuing, you’ll find that
you don’t need to litter your program with locks and other low-level synchronization.
Also, communicating with queues often leads to designs that can be scaled up to other
kinds of message-based communication patterns later on. For instance, you might be

able to split your program into multiple processes, or even a distributed system, without
changing much of its underlying queuing architecture.
One caution with thread queues is that putting an item in a queue doesn’t make a copy
of the item. Thus, communication actually involves passing an object reference between
threads. If you are concerned about shared state, it may make sense to only pass im‐
mutable data structures (e.g., integers, strings, or tuples) or to make deep copies of the
queued items. For example:
from queue import Queue
from threading import Thread
import copy

# A thread that produces data
def producer(out_q):
    while True:
        # Produce some data
        ...
        out_q.put(copy.deepcopy(data))

# A thread that consumes data
def consumer(in_q):
    while True:
        # Get some data
        data = in_q.get()
        # Process the data
        ...

Queue objects provide a few additional features that may prove to be useful in certain
contexts. If you create a Queue with an optional size, such as Queue(N), it places a limit
on the number of items that can be enqueued before the put() blocks the producer.
Adding an upper bound to a queue might make sense if there is mismatch in speed
between a producer and consumer. For instance, if a producer is generating items at a
much faster rate than they can be consumed. On the other hand, making a queue block
when it’s full can also have an unintended cascading effect throughout your program,
possibly causing it to deadlock or run poorly. In general, the problem of “flow control”
between communicating threads is a much harder problem than it seems. If you ever
find yourself trying to fix a problem by fiddling with queue sizes, it could be an indicator
of a fragile design or some other inherent scaling problem.
Both the get() and put() methods support nonblocking and timeouts. For example:

import queue
q = queue.Queue()

try:
    data = q.get(block=False)
except queue.Empty:
    ...

try:
    q.put(item, block=False)
except queue.Full:
    ...

try:
    data = q.get(timeout=5.0)
except queue.Empty:
    ...

Both of these options can be used to avoid the problem of just blocking indefinitely on
a particular queuing operation. For example, a nonblocking put() could be used with
a fixed-sized queue to implement different kinds of handling code for when a queue is
full. For example, issuing a log message and discarding:

def producer(q):
    ...
    try:
        q.put(item, block=False)
    except queue.Full:
        log.warning('queued item %r discarded!', item)

A timeout is useful if you’re trying to make consumer threads periodically give up on
operations such as q.get() so that they can check things such as a termination flag, as
described in Recipe 12.1.

_running = True

def consumer(q):
    while _running:
        try:
            item = q.get(timeout=5.0)
            # Process item
            ...
        except queue.Empty:
            pass

Lastly, there are utility methods q.qsize(), q.full(), q.empty() that can tell you the
current size and status of the queue. However, be aware that all of these are unreliable
in a multithreaded environment. For example, a call to q.empty() might tell you that
the queue is empty, but in the time that has elapsed since making the call, another thread
could have added an item to the queue. Frankly, it’s best to write your code not to rely
on such functions.

