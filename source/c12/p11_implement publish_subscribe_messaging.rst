============================
12.11 实现消息发布/订阅模型
============================

----------
问题
----------
You have a program based on communicating threads and want them to implement
publish/subscribe messaging.

Solution
To  implement  publish/subscribe  messaging,  you  typically  introduce  a  separate  “ex‐
change” or “gateway” object that acts as an intermediary for all messages. That is, instead
of directly sending a message from one task to another, a message is sent to the exchange
and it delivers it to one or more attached tasks. Here is one example of a very simple
exchange implementation:

from collections import defaultdict

class Exchange:
    def __init__(self):
        self._subscribers = set()

    def attach(self, task):
        self._subscribers.add(task)

    def detach(self, task):
        self._subscribers.remove(task)

    def send(self, msg):
        for subscriber in self._subscribers:
            subscriber.send(msg)

# Dictionary of all created exchanges
_exchanges = defaultdict(Exchange)

# Return the Exchange instance associated with a given name
def get_exchange(name):
    return _exchanges[name]

An exchange is really nothing more than an object that keeps a set of active subscribers
and provides methods for attaching, detaching, and sending messages. Each exchange
is  identified  by  a  name,  and  the  get_exchange()  function  simply  returns  the  Ex
change instance associated with a given name.
Here is a simple example that shows how to use an exchange:

# Example of a task.  Any object with a send() method

class Task:
    ...
    def send(self, msg):
        ...

task_a = Task()
task_b = Task()

# Example of getting an exchange
exc = get_exchange('name')

# Examples of subscribing tasks to it
exc.attach(task_a)
exc.attach(task_b)

# Example of sending messages
exc.send('msg1')
exc.send('msg2')

# Example of unsubscribing
exc.detach(task_a)
exc.detach(task_b)

Although there are many different variations on this theme, the overall idea is the same.
Messages will be delivered to an exchange and the exchange will deliver them to attached
subscribers.

Discussion
The concept of tasks or threads sending messages to one another (often via queues) is
easy to implement and quite popular. However, the benefits of using a public/subscribe
(pub/sub) model instead are often overlooked.
First, the use of an exchange can simplify much of the plumbing involved in setting up
communicating threads. Instead of trying to wire threads together across multiple pro‐
gram modules, you only worry about connecting them to a known exchange. In some
sense, this is similar to how the logging library works. In practice, it can make it easier
to decouple various tasks in the program.
Second, the ability of the exchange to broadcast messages to multiple subscribers opens
up new communication patterns. For example, you could implement systems with re‐
dundant tasks, broadcasting, or fan-out. You could also build debugging and diagnostic
tools that attach themselves to exchanges as ordinary subscribers. For example, here is
a simple diagnostic class that would display sent messages:

class DisplayMessages:
    def __init__(self):
        self.count = 0
    def send(self, msg):
        self.count += 1
        print('msg[{}]: {!r}'.format(self.count, msg))

exc = get_exchange('name')
d = DisplayMessages()
exc.attach(d)

Last, but not least, a notable aspect of the implementation is that it works with a variety
of task-like objects. For example, the receivers of a message could be actors (as described
in Recipe 12.10), coroutines, network connections, or just about anything that imple‐
ments a proper send() method.
One potentially problematic aspect of an exchange concerns the proper attachment and
detachment of subscribers. In order to properly manage resources, every subscriber that
attaches must eventually detach. This leads to a programming model similar to this:

exc = get_exchange('name')
exc.attach(some_task)
try:
    ...
finally:
    exc.detach(some_task)

In some sense, this is similar to the usage of files, locks, and similar objects. Experience
has shown that it is quite easy to forget the final detach() step. To simplify this, you
might consider the use of the context-management protocol. For example, adding a
subscribe() method to the exchange like this:

from contextlib import contextmanager
from collections import defaultdict

class Exchange:
    def __init__(self):
        self._subscribers = set()

    def attach(self, task):
        self._subscribers.add(task)

    def detach(self, task):
        self._subscribers.remove(task)

    @contextmanager
    def subscribe(self, *tasks):
        for task in tasks:
            self.attach(task)
        try:
            yield
        finally:
            for task in tasks:
                self.detach(task)

    def send(self, msg):
        for subscriber in self._subscribers:
            subscriber.send(msg)

# Dictionary of all created exchanges
_exchanges = defaultdict(Exchange)

# Return the Exchange instance associated with a given name
def get_exchange(name):
    return _exchanges[name]

# Example of using the subscribe() method
exc = get_exchange('name')
with exc.subscribe(task_a, task_b):
     ...
     exc.send('msg1')
     exc.send('msg2')
     ...

# task_a and task_b detached here

Finally, it should be noted that there are numerous possible extensions to the exchange
idea. For example, exchanges could implement an entire collection of message channels

or apply pattern matching rules to exchange names. Exchanges can also be extended
into distributed computing applications (e.g., routing messages to tasks on different
machines, etc.).
