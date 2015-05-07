==============================
11.12 理解事件驱动的IO
==============================

----------
问题
----------
You have heard about packages based on “event-driven” or “asynchronous” I/O, but
you’re not entirely sure what it means, how it actually works under the covers, or how
it might impact your program if you use it.

Solution
At a fundamental level, event-driven I/O is a technique that takes basic I/O operations
(e.g., reads and writes) and converts them into events that must be handled by your
program. For example, whenever data was received on a socket, it turns into a “receive”
event that is handled by some sort of callback method or function that you supply to
respond to it. As a possible starting point, an event-driven framework might start with
a base class that implements a series of basic event handler methods like this:

class EventHandler:
    def fileno(self):
        'Return the associated file descriptor'
        raise NotImplemented('must implement')

    def wants_to_receive(self):
        'Return True if receiving is allowed'
        return False

    def handle_receive(self):
        'Perform the receive operation'
        pass

    def wants_to_send(self):
        'Return True if sending is requested'
        return False

    def handle_send(self):
        'Send outgoing data'
        pass

Instances of this class then get plugged into an event loop that looks like this:

import select

def event_loop(handlers):
    while True:
        wants_recv = [h for h in handlers if h.wants_to_receive()]
        wants_send = [h for h in handlers if h.wants_to_send()]
        can_recv, can_send, _ = select.select(wants_recv, wants_send, [])
        for h in can_recv:
            h.handle_receive()
        for h in can_send:
            h.handle_send()

That’s it! The key to the event loop is the select() call, which polls file descriptors for
activity. Prior to calling select(), the event loop simply queries all of the handlers to
see which ones want to receive or send. It then supplies the resulting lists to select().
As a result, select() returns the list of objects that are ready to receive or send. The
corresponding handle_receive() or handle_send() methods are triggered.
To write applications, specific instances of EventHandler classes are created. For ex‐
ample, here are two simple handlers that illustrate two UDP-based network services:

import socket
import time

class UDPServer(EventHandler):
    def __init__(self, address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(address)

    def fileno(self):
        return self.sock.fileno()

    def wants_to_receive(self):
        return True

class UDPTimeServer(UDPServer):
    def handle_receive(self):
        msg, addr = self.sock.recvfrom(1)
        self.sock.sendto(time.ctime().encode('ascii'), addr)

class UDPEchoServer(UDPServer):
    def handle_receive(self):
        msg, addr = self.sock.recvfrom(8192)
        self.sock.sendto(msg, addr)

if __name__ == '__main__':
    handlers = [ UDPTimeServer(('',14000)), UDPEchoServer(('',15000))  ]
    event_loop(handlers)

To test this code, you can try connecting to it from another Python interpreter:

>>> from socket import *
>>> s = socket(AF_INET, SOCK_DGRAM)
>>> s.sendto(b'',('localhost',14000))
0
>>> s.recvfrom(128)
(b'Tue Sep 18 14:29:23 2012', ('127.0.0.1', 14000))
>>> s.sendto(b'Hello',('localhost',15000))
5
>>> s.recvfrom(128)
(b'Hello', ('127.0.0.1', 15000))
>>>

Implementing a TCP server is somewhat more complex, since each client involves the
instantiation of a new handler object. Here is an example of a TCP echo client.

class TCPServer(EventHandler):
    def __init__(self, address, client_handler, handler_list):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.sock.bind(address)
        self.sock.listen(1)
        self.client_handler = client_handler
        self.handler_list = handler_list

    def fileno(self):
        return self.sock.fileno()

    def wants_to_receive(self):
        return True

    def handle_receive(self):
        client, addr = self.sock.accept()
        # Add the client to the event loop's handler list
        self.handler_list.append(self.client_handler(client, self.handler_list))

class TCPClient(EventHandler):
    def __init__(self, sock, handler_list):
        self.sock = sock
        self.handler_list = handler_list
        self.outgoing = bytearray()

    def fileno(self):
        return self.sock.fileno()

    def close(self):
        self.sock.close()
        # Remove myself from the event loop's handler list
        self.handler_list.remove(self)

    def wants_to_send(self):
        return True if self.outgoing else False

    def handle_send(self):
        nsent = self.sock.send(self.outgoing)
        self.outgoing = self.outgoing[nsent:]

class TCPEchoClient(TCPClient):
    def wants_to_receive(self):
        return True

    def handle_receive(self):
        data = self.sock.recv(8192)
        if not data:
            self.close()
        else:
            self.outgoing.extend(data)

if __name__ == '__main__':
   handlers = []
   handlers.append(TCPServer(('',16000), TCPEchoClient, handlers))
   event_loop(handlers)

The key to the TCP example is the addition and removal of clients from the handler list.
On each connection, a new handler is created for the client and added to the list. When
the connection is closed, each client must take care to remove themselves from the list.
If you run this program and try connecting with Telnet or some similar tool, you’ll see
it echoing received data back to you. It should easily handle multiple clients.

Discussion
Virtually all event-driven frameworks operate in a manner that is similar to that shown
in the solution. The actual implementation details and overall software architecture
might vary greatly, but at the core, there is a polling loop that checks sockets for activity
and which performs operations in response.
One potential benefit of event-driven I/O is that it can handle a very large number of
simultaneous  connections  without  ever  using  threads  or  processes.  That  is,  the  se
lect() call (or equivalent) can be used to monitor hundreds or thousands of sockets
and respond to events occuring on any of them. Events are handled one at a time by the
event loop, without the need for any other concurrency primitives.
The downside to event-driven I/O is that there is no true concurrency involved. If any
of the event handler methods blocks or performs a long-running calculation, it blocks
the progress of everything. There is also the problem of calling out to library functions
that aren’t written in an event-driven style. There is always the risk that some library
call will block, causing the event loop to stall.
Problems with blocking or long-running calculations can be solved by sending the work
out to a separate thread or process. However, coordinating threads and processes with
an event loop is tricky. Here is an example of code that will do it using the  concur
rent.futures module:

from concurrent.futures import ThreadPoolExecutor
import os

class ThreadPoolHandler(EventHandler):
    def __init__(self, nworkers):
        if os.name == 'posix':
            self.signal_done_sock, self.done_sock = socket.socketpair()
        else:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(('127.0.0.1', 0))
            server.listen(1)
            self.signal_done_sock = socket.socket(socket.AF_INET,
                                                  socket.SOCK_STREAM)
            self.signal_done_sock.connect(server.getsockname())
            self.done_sock, _ = server.accept()
            server.close()

        self.pending = []
        self.pool = ThreadPoolExecutor(nworkers)

    def fileno(self):
        return self.done_sock.fileno()

    # Callback that executes when the thread is done
    def _complete(self, callback, r):

        self.pending.append((callback, r.result()))
        self.signal_done_sock.send(b'x')

    # Run a function in a thread pool
    def run(self, func, args=(), kwargs={},*,callback):
        r = self.pool.submit(func, *args, **kwargs)
        r.add_done_callback(lambda r: self._complete(callback, r))

    def wants_to_receive(self):
        return True

    # Run callback functions of completed work
    def handle_receive(self):
        # Invoke all pending callback functions
        for callback, result in self.pending:
            callback(result)
            self.done_sock.recv(1)
        self.pending = []

In this code, the run() method is used to submit work to the pool along with a callback
function that should be triggered upon completion. The actual work is then submitted
to a ThreadPoolExecutor instance. However, a really tricky problem concerns the co‐
ordination of the computed result and the event loop. To do this, a pair of sockets are
created under the covers and used as a kind of signaling mechanism. When work is
completed by the thread pool, it executes the _complete() method in the class. This
method queues up the pending callback and result before writing a byte of data on one
of these sockets. The fileno() method is programmed to return the other socket. Thus,
when this byte is written, it will signal to the event loop that something has happened.
The handle_receive() method, when triggered, will then execute all of the callback
functions for previously submitted work. Frankly, it’s enough to make one’s head spin.
Here is a simple server that shows how to use the thread pool to carry out a long-running
calculation:

# A really bad Fibonacci implementation
def fib(n):
    if n < 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

class UDPFibServer(UDPServer):
    def handle_receive(self):
        msg, addr = self.sock.recvfrom(128)
        n = int(msg)
        pool.run(fib, (n,), callback=lambda r: self.respond(r, addr))

    def respond(self, result, addr):
        self.sock.sendto(str(result).encode('ascii'), addr)

if __name__ == '__main__':
    pool = ThreadPoolHandler(16)
    handlers = [ pool, UDPFibServer(('',16000))]
    event_loop(handlers)

To try this server, simply run it and try some experiments with another Python program:

from socket import *
sock = socket(AF_INET, SOCK_DGRAM)
for x in range(40):
    sock.sendto(str(x).encode('ascii'), ('localhost', 16000))
    resp = sock.recvfrom(8192)
    print(resp[0])

You should be able to run this program repeatedly from many different windows and
have it operate without stalling other programs, even though it gets slower and slower
as the numbers get larger.
Having gone through this recipe, should you use its code? Probably not. Instead, you
should look for a more fully developed framework that accomplishes the same task.
However, if you understand the basic concepts presented here, you’ll understand the
core techniques used to make such frameworks operate. As an alternative to callback-
based programming, event-driven code will sometimes use coroutines. See Recipe 12.12
for an example.
