===============================
11.7 在不同的Python解释器之间交互
===============================

----------
问题
----------
You are running multiple instances of the Python interpreter, possibly on different ma‐
chines, and you would like to exchange data between interpreters using messages.

Solution
It is easy to communicate between interpreters if you use the multiprocessing.con
nection module. Here is a simple example of writing an echo server:

from multiprocessing.connection import Listener
import traceback

def echo_client(conn):
    try:
        while True:
            msg = conn.recv()
            conn.send(msg)
    except EOFError:
        print('Connection closed')

def echo_server(address, authkey):
    serv = Listener(address, authkey=authkey)
    while True:
        try:
            client = serv.accept()

            echo_client(client)
        except Exception:
            traceback.print_exc()

echo_server(('', 25000), authkey=b'peekaboo')

Here  is  a  simple  example  of  a  client  connecting  to  the  server  and  sending  various
messages:

>>> from multiprocessing.connection import Client
>>> c = Client(('localhost', 25000), authkey=b'peekaboo')
>>> c.send('hello')
>>> c.recv()
'hello'
>>> c.send(42)
>>> c.recv()
42
>>> c.send([1, 2, 3, 4, 5])
>>> c.recv()
[1, 2, 3, 4, 5]
>>>

Unlike a low-level socket, messages are kept intact (each object sent using send() is
received in its entirety with recv()). In addition, objects are serialized using pickle.
So, any object compatible with pickle can be sent or received over the connection.

Discussion
There are many packages and libraries related to implementing various forms of mes‐
sage passing, such as ZeroMQ, Celery, and so forth. As an alternative, you might also
be inclined to implement a message layer on top of low-level sockets. However, some‐
times you just want a simple solution. The multiprocessing.connection library is just
that—using a few simple primitives, you can easily connect interpreters together and
have them exchange messages.
If you know that the interpreters are going to be running on the same machine, you can
use alternative forms of networking, such as UNIX domain sockets or Windows named
pipes. To create a connection using a UNIX domain socket, simply change the address
to a filename such as this:

s = Listener('/tmp/myconn', authkey=b'peekaboo')

To create a connection using a Windows named pipe, use a filename such as this:

s = Listener(r'\\.\pipe\myconn', authkey=b'peekaboo')

As a general rule, you would not be using multiprocessing to implement public-facing
services. The authkey parameter to Client() and Listener() is there to help authen‐
ticate the end points of the connection. Connection attempts with a bad key raise an
exception. In addition, the module is probably best suited for long-running connections

(not a large number of short connections). For example, two interpreters might establish
a connection at startup and keep the connection active for the entire duration of a
problem.
Don’t use multiprocessing if you need more low-level control over aspects of the con‐
nection. For example, if you needed to support timeouts, nonblocking I/O, or anything
similar, you’re probably better off using a different library or implementing such features
on top of sockets instead.
