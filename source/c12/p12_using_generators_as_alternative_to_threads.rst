============================
12.12 使用生成器代替线程
============================

----------
问题
----------
You want to implement concurrency using generators (coroutines) as an alternative to
system threads. This is sometimes known as user-level threading or green threading.

Solution
To implement your own concurrency using generators, you first need a fundamental
insight concerning generator functions and the yield statement. Specifically, the fun‐
damental behavior of yield is that it causes a generator to suspend its execution. By
suspending execution, it is possible to write a scheduler that treats generators as a kind
of “task” and alternates their execution using a kind of cooperative task switching.
To illustrate this idea, consider the following two generator functions using a simple
yield:

# Two simple generator functions
def countdown(n):
    while n > 0:
        print('T-minus', n)
        yield
        n -= 1
    print('Blastoff!')

def countup(n):
    x = 0
    while x < n:
        print('Counting up', x)
        yield
        x += 1

These functions probably look a bit funny using yield all by itself. However, consider
the following code that implements a simple task scheduler:

from collections import deque

class TaskScheduler:
    def __init__(self):
        self._task_queue = deque()

    def new_task(self, task):
        '''
        Admit a newly started task to the scheduler

        '''
        self._task_queue.append(task)

    def run(self):
        '''
        Run until there are no more tasks
        '''
        while self._task_queue:
            task = self._task_queue.popleft()
            try:
                # Run until the next yield statement
                next(task)
                self._task_queue.append(task)
            except StopIteration:
                # Generator is no longer executing
                pass

# Example use
sched = TaskScheduler()
sched.new_task(countdown(10))
sched.new_task(countdown(5))
sched.new_task(countup(15))
sched.run()

In this code, the TaskScheduler class runs a collection of generators in a round-robin
manner—each one running until they reach a  yield statement. For the sample, the
output will be as follows:

T-minus 10
T-minus 5
Counting up 0
T-minus 9
T-minus 4
Counting up 1
T-minus 8
T-minus 3
Counting up 2
T-minus 7
T-minus 2
...

At this point, you’ve essentially implemented the tiny core of an “operating system” if
you will. Generator functions are the tasks and the yield statement is how tasks signal
that they want to suspend. The scheduler simply cycles over the tasks until none are left
executing.
In practice, you probably wouldn’t use generators to implement concurrency for some‐
thing as simple as shown. Instead, you might use generators to replace the use of threads
when implementing actors (see Recipe 12.10) or network servers.

The following code illustrates the use of generators to implement a thread-free version
of actors:

from collections import deque

class ActorScheduler:
    def __init__(self):
        self._actors = { }          # Mapping of names to actors
        self._msg_queue = deque()   # Message queue

    def new_actor(self, name, actor):
        '''
        Admit a newly started actor to the scheduler and give it a name
        '''
        self._msg_queue.append((actor,None))
        self._actors[name] = actor

    def send(self, name, msg):
        '''
        Send a message to a named actor
        '''
        actor = self._actors.get(name)
        if actor:
            self._msg_queue.append((actor,msg))

    def run(self):
        '''
        Run as long as there are pending messages.
        '''
        while self._msg_queue:
            actor, msg = self._msg_queue.popleft()
            try:
                 actor.send(msg)
            except StopIteration:
                 pass

# Example use
if __name__ == '__main__':
    def printer():
        while True:
            msg = yield
            print('Got:', msg)

    def counter(sched):
        while True:
            # Receive the current count
            n = yield
            if n == 0:
                break
            # Send to the printer task
            sched.send('printer', n)
            # Send the next count to the counter task (recursive)

            sched.send('counter', n-1)

    sched = ActorScheduler()
    # Create the initial actors
    sched.new_actor('printer', printer())
    sched.new_actor('counter', counter(sched))

    # Send an initial message to the counter to initiate
    sched.send('counter', 10000)
    sched.run()

The execution of this code might take a bit of study, but the key is the queue of pending
messages. Essentially, the scheduler runs as long as there are messages to deliver. A
remarkable feature is that the counter generator sends messages to itself and ends up
in a recursive cycle not bound by Python’s recursion limit.
Here is an advanced example showing the use of generators to implement a concurrent
network application:

from collections import deque
from select import select

# This class represents a generic yield event in the scheduler
class YieldEvent:
    def handle_yield(self, sched, task):
        pass
    def handle_resume(self, sched, task):
        pass

# Task Scheduler
class Scheduler:
    def __init__(self):
        self._numtasks = 0       # Total num of tasks
        self._ready = deque()    # Tasks ready to run
        self._read_waiting = {}  # Tasks waiting to read
        self._write_waiting = {} # Tasks waiting to write

    # Poll for I/O events and restart waiting tasks
    def _iopoll(self):
        rset,wset,eset = select(self._read_waiting,
                                self._write_waiting,[])
        for r in rset:
            evt, task = self._read_waiting.pop(r)
            evt.handle_resume(self, task)
        for w in wset:
            evt, task = self._write_waiting.pop(w)
            evt.handle_resume(self, task)

    def new(self,task):
        '''
        Add a newly started task to the scheduler
        '''

        self._ready.append((task, None))
        self._numtasks += 1

    def add_ready(self, task, msg=None):
        '''
        Append an already started task to the ready queue.
        msg is what to send into the task when it resumes.
        '''
        self._ready.append((task, msg))

    # Add a task to the reading set
    def _read_wait(self, fileno, evt, task):
        self._read_waiting[fileno] = (evt, task)

    # Add a task to the write set
    def _write_wait(self, fileno, evt, task):
        self._write_waiting[fileno] = (evt, task)

    def run(self):
        '''
        Run the task scheduler until there are no tasks
        '''
        while self._numtasks:
             if not self._ready:
                  self._iopoll()
             task, msg = self._ready.popleft()
             try:
                 # Run the coroutine to the next yield
                 r = task.send(msg)
                 if isinstance(r, YieldEvent):
                     r.handle_yield(self, task)
                 else:
                     raise RuntimeError('unrecognized yield event')
             except StopIteration:
                 self._numtasks -= 1

# Example implementation of coroutine-based socket I/O
class ReadSocket(YieldEvent):
    def __init__(self, sock, nbytes):
        self.sock = sock
        self.nbytes = nbytes
    def handle_yield(self, sched, task):
        sched._read_wait(self.sock.fileno(), self, task)
    def handle_resume(self, sched, task):
        data = self.sock.recv(self.nbytes)
        sched.add_ready(task, data)

class WriteSocket(YieldEvent):
    def __init__(self, sock, data):
        self.sock = sock
        self.data = data
    def handle_yield(self, sched, task):

        sched._write_wait(self.sock.fileno(), self, task)
    def handle_resume(self, sched, task):
        nsent = self.sock.send(self.data)
        sched.add_ready(task, nsent)

class AcceptSocket(YieldEvent):
    def __init__(self, sock):
        self.sock = sock
    def handle_yield(self, sched, task):
        sched._read_wait(self.sock.fileno(), self, task)
    def handle_resume(self, sched, task):
        r = self.sock.accept()
        sched.add_ready(task, r)

# Wrapper around a socket object for use with yield
class Socket(object):
    def __init__(self, sock):
        self._sock = sock
    def recv(self, maxbytes):
        return ReadSocket(self._sock, maxbytes)
    def send(self, data):
        return WriteSocket(self._sock, data)
    def accept(self):
        return AcceptSocket(self._sock)
    def __getattr__(self, name):
        return getattr(self._sock, name)

if __name__ == '__main__':
    from socket import socket, AF_INET, SOCK_STREAM
    import time

    # Example of a function involving generators.  This should
    # be called using line = yield from readline(sock)
    def readline(sock):
        chars = []
        while True:
            c = yield sock.recv(1)
            if not c:
                break
            chars.append(c)
            if c == b'\n':
                break
        return b''.join(chars)

    # Echo server using generators
    class EchoServer:
        def __init__(self,addr,sched):
            self.sched = sched
            sched.new(self.server_loop(addr))

        def server_loop(self,addr):
            s = Socket(socket(AF_INET,SOCK_STREAM))

            s.bind(addr)
            s.listen(5)
            while True:
                c,a = yield s.accept()
                print('Got connection from ', a)
                self.sched.new(self.client_handler(Socket(c)))

        def client_handler(self,client):
            while True:
                line = yield from readline(client)
                if not line:
                    break
                line = b'GOT:' + line
                while line:
                    nsent = yield client.send(line)
                    line = line[nsent:]
            client.close()
            print('Client closed')

    sched = Scheduler()
    EchoServer(('',16000),sched)
    sched.run()

This code will undoubtedly require a certain amount of careful study. However, it is
essentially implementing a small operating system. There is a queue of tasks ready to
run and there are waiting areas for tasks sleeping for I/O. Much of the scheduler involves
moving tasks between the ready queue and the I/O waiting area.

Discussion
When building generator-based concurrency frameworks, it is most common to work
with the more general form of yield:

def some_generator():
    ...
    result = yield data
    ...

Functions that use yield in this manner are more generally referred to as “coroutines.”
Within a scheduler, the yield statement gets handled in a loop as follows:

f = some_generator()

# Initial result. Is None to start since nothing has been computed
result = None
while True:
    try:
        data = f.send(result)
        result = ... do some calculation ...
    except StopIteration:
        break

The logic concerning the result is a bit convoluted. However, the value passed to send()
defines what gets returned when the yield statement wakes back up. So, if a yield is
going to return a result in response to data that was previously yielded, it gets returned
on the next send() operation. If a generator function has just started, sending in a value
of None simply makes it advance to the first yield statement.
In addition to sending in values, it is also possible to execute a close() method on a
generator. This causes a silent GeneratorExit exception to be raised at the yield state‐
ment, which stops execution. If desired, a generator can catch this exception and per‐
form cleanup actions. It’s also possible to use the throw() method of a generator to raise
an arbitrary execution at the yield statement. A task scheduler might use this to com‐
municate errors into running generators.
The yield from statement used in the last example is used to implement coroutines
that serve as subroutines or procedures to be called from other generators. Essentially,
control transparently transfers to the new function. Unlike normal generators, a func‐
tion that is called using yield from can return a value that becomes the result of the
yield from statement. More information about yield from can be found in PEP 380.
Finally, if programming with generators, it is important to stress that there are some
major limitations. In particular, you get none of the benefits that threads provide. For
instance, if you execute any code that is CPU bound or which blocks for I/O, it will
suspend the entire task scheduler until the completion of that operation. To work around
this, your only real option is to delegate the operation to a separate thread or process
where it can run independently. Another limitation is that most Python libraries have
not been written to work well with generator-based threading. If you take this approach,
you may find that you need to write replacements for many standard library functions.
As basic background on coroutines and the techniques utilized in this recipe, see PEP
342 and “A Curious Course on Coroutines and Concurrency”.
PEP 3156 also has a modern take on asynchronous I/O involving coroutines. In practice,
it  is  extremelyunlikely  that  you  will  write  a  low-level  coroutine  scheduler  yourself.
However, ideas surrounding coroutines are the basis for many popular libraries, in‐
cluding gevent, greenlet, Stackless Python, and similar projects.
