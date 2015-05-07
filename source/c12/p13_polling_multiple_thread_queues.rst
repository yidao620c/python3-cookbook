============================
12.13 多个线程队列轮询
============================

----------
问题
----------
You have a collection of thread queues, and you would like to be able to poll them for
incoming items, much in the same way as you might poll a collection of network con‐
nections for incoming data.

Solution
A common solution to polling problems involves a little-known trick involving a hidden
loopback network connection. Essentially, the idea is as follows: for each queue (or any
object) that you want to poll, you create a pair of connected sockets. You then write on
one of the sockets to signal the presence of data. The other sockect is then passed to
select() or a similar function to poll for the arrival of data. Here is some sample code
that illustrates this idea:

import queue
import socket
import os

class PollableQueue(queue.Queue):
    def __init__(self):
        super().__init__()
        # Create a pair of connected sockets
        if os.name == 'posix':
            self._putsocket, self._getsocket = socket.socketpair()
        else:
            # Compatibility on non-POSIX systems
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(('127.0.0.1', 0))
            server.listen(1)
            self._putsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._putsocket.connect(server.getsockname())
            self._getsocket, _ = server.accept()
            server.close()

    def fileno(self):
        return self._getsocket.fileno()

    def put(self, item):
        super().put(item)
        self._putsocket.send(b'x')

    def get(self):
        self._getsocket.recv(1)
        return super().get()

In this code, a new kind of Queue instance is defined where there is an underlying pair
of connected sockets. The socketpair() function on Unix machines can establish such
sockets easily. On Windows, you have to fake it using code similar to that shown (it
looks a bit weird, but a server socket is created and a client immediately connects to it
afterward). The normal get() and put() methods are then redefined slightly to perform
a small bit of I/O on these sockets. The put() method writes a single byte of data to one
of the sockets after putting data on the queue. The get() method reads a single byte of
data from the other socket when removing an item from the queue.

The fileno() method is what makes the queue pollable using a function such as se
lect(). Essentially, it just exposes the underlying file descriptor of the socket used by
the get() function.
Here is an example of some code that defines a consumer which monitors multiple
queues for incoming items:

import select
import threading

def consumer(queues):
    '''
    Consumer that reads data on multiple queues simultaneously
    '''
    while True:
        can_read, _, _ = select.select(queues,[],[])
        for r in can_read:
            item = r.get()
            print('Got:', item)

q1 = PollableQueue()
q2 = PollableQueue()
q3 = PollableQueue()
t = threading.Thread(target=consumer, args=([q1,q2,q3],))
t.daemon = True
t.start()

# Feed data to the queues
q1.put(1)
q2.put(10)
q3.put('hello')
q2.put(15)
...

If you try it, you’ll find that the consumer indeed receives all of the put items, regardless
of which queues they are placed in.

Discussion
The problem of polling non-file-like objects, such as queues, is often a lot trickier than
it looks. For instance, if you don’t use the socket technique shown, your only option is
to write code that cycles through the queues and uses a timer, like this:

import time
def consumer(queues):
    while True:
        for q in queues:
            if not q.empty():
                item = q.get()
                print('Got:', item)

        # Sleep briefly to avoid 100% CPU
        time.sleep(0.01)

This might work for certain kinds of problems, but it’s clumsy and introduces other
weird performance problems. For example, if new data is added to a queue, it won’t be
detected for as long as 10 milliseconds (an eternity on a modern processor).
You run into even further problems if the preceding polling is mixed with the polling
of other objects, such as network sockets. For example, if you want to poll both sockets
and queues at the same time, you might have to use code like this:

import select

def event_loop(sockets, queues):
    while True:
        # polling with a timeout
        can_read, _, _ = select.select(sockets, [], [], 0.01)
        for r in can_read:
            handle_read(r)
        for q in queues:
            if not q.empty():
                item = q.get()
                print('Got:', item)

The solution shown solves a lot of these problems by simply putting queues on equal
status with sockets. A single select() call can be used to poll for activity on both. It is
not necessary to use timeouts or other time-based hacks to periodically check. More‐
over, if data gets added to a queue, the consumer will be notified almost instantaneously.
Although there is a tiny amount of overhead associated with the underlying I/O, it often
is worth it to have better response time and simplified coding.
