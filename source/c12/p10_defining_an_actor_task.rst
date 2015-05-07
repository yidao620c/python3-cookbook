============================
12.10 定义一个Actor任务
============================

----------
问题
----------
You’d like to define tasks with behavior similar to “actors” in the so-called “actor model.”

Solution
The “actor model” is one of the oldest and most simple approaches to concurrency and
distributed computing. In fact, its underlying simplicity is part of its appeal. In a nutshell,
an actor is a concurrently executing task that simply acts upon messages sent to it. In
response to these messages, it may decide to send further messages to other actors.
Communication with actors is one way and asynchronous. Thus, the sender of a message
does not know when a message actually gets delivered, nor does it receive a response
or acknowledgment that the message has been processed.
Actors are straightforward to define using a combination of a thread and a queue. For
example:

from queue import Queue
from threading import Thread, Event

# Sentinel used for shutdown
class ActorExit(Exception):
    pass

class Actor:
    def __init__(self):
        self._mailbox = Queue()

    def send(self, msg):
        '''
        Send a message to the actor
        '''
        self._mailbox.put(msg)

    def recv(self):
        '''
        Receive an incoming message
        '''
        msg = self._mailbox.get()
        if msg is ActorExit:
            raise ActorExit()
        return msg

    def close(self):
        '''
        Close the actor, thus shutting it down
        '''
        self.send(ActorExit)

    def start(self):
        '''
        Start concurrent execution
        '''
        self._terminated = Event()
        t = Thread(target=self._bootstrap)

        t.daemon = True
        t.start()

    def _bootstrap(self):
        try:
            self.run()
        except ActorExit:
            pass
        finally:
            self._terminated.set()

    def join(self):
        self._terminated.wait()

    def run(self):
        '''
        Run method to be implemented by the user
        '''
        while True:
            msg = self.recv()

# Sample ActorTask
class PrintActor(Actor):
    def run(self):
        while True:
            msg = self.recv()
            print('Got:', msg)

# Sample use
p = PrintActor()
p.start()
p.send('Hello')
p.send('World')
p.close()
p.join()

In this example, Actor instances are things that you simply send a message to using
their send() method. Under the covers, this places the message on a queue and hands
it off to an internal thread that runs to process the received messages. The close()
method  is  programmed  to  shut  down  the  actor  by  placing  a  special  sentinel  value
(ActorExit) on the queue. Users define new actors by inheriting from Actor and re‐
defining the run() method to implement their custom processing. The usage of the
ActorExit exception is such that user-defined code can be programmed to catch the
termination request and handle it if appropriate (the exception is raised by the get()
method and propagated).
If you relax the requirement of concurrent and asynchronous message delivery, actor-
like objects can also be minimally defined by generators. For example:

def print_actor():
    while True:

        try:
            msg = yield      # Get a message
            print('Got:', msg)
        except GeneratorExit:
            print('Actor terminating')

# Sample use
p = print_actor()
next(p)     # Advance to the yield (ready to receive)
p.send('Hello')
p.send('World')
p.close()

Discussion
Part of the appeal of actors is their underlying simplicity. In practice, there is just one
core operation, send(). Plus, the general concept of a “message” in actor-based systems
is something that can be expanded in many different directions. For example, you could
pass tagged messages in the form of tuples and have actors take different courses of
action like this:

class TaggedActor(Actor):
    def run(self):
        while True:
             tag, *payload = self.recv()
             getattr(self,'do_'+tag)(*payload)

    # Methods correponding to different message tags
    def do_A(self, x):
        print('Running A', x)

    def do_B(self, x, y):
        print('Running B', x, y)

# Example
a = TaggedActor()
a.start()
a.send(('A', 1))      # Invokes do_A(1)
a.send(('B', 2, 3))   # Invokes do_B(2,3)

As another example, here is a variation of an actor that allows arbitrary functions to be
executed in a worker and results to be communicated back using a special Result object:

from threading import Event
class Result:
    def __init__(self):
        self._evt = Event()
        self._result = None

    def set_result(self, value):
        self._result = value

        self._evt.set()

    def result(self):
        self._evt.wait()
        return self._result

class Worker(Actor):
    def submit(self, func, *args, **kwargs):
        r = Result()
        self.send((func, args, kwargs, r))
        return r

    def run(self):
        while True:
            func, args, kwargs, r = self.recv()
            r.set_result(func(*args, **kwargs))

# Example use
worker = Worker()
worker.start()
r = worker.submit(pow, 2, 3)
print(r.result())

Last, but not least, the concept of “sending” a task a message is something that can be
scaled up into systems involving multiple processes or even large distributed systems.
For example, the send() method of an actor-like object could be programmed to trans‐
mit data on a socket connection or deliver it via some kind of messaging infrastructure
(e.g., AMQP, ZMQ, etc.).
