===============================
11.8 实现远程方法调用
===============================

----------
问题
----------
You want to implement simple remote procedure call (RPC) on top of a message passing
layer, such as sockets, multiprocessing connections, or ZeroMQ.

|

----------
解决方案
----------
RPC is easy to implement by encoding function requests, arguments, and return values
using  pickle, and passing the pickled byte strings between interpreters. Here is an
example of a simple RPC handler that could be incorporated into a server:

# rpcserver.py

import pickle
class RPCHandler:
    def __init__(self):
        self._functions = { }

    def register_function(self, func):
        self._functions[func.__name__] = func

    def handle_connection(self, connection):
        try:
            while True:
                # Receive a message
                func_name, args, kwargs = pickle.loads(connection.recv())
                # Run the RPC and send a response
                try:
                    r = self._functions[func_name](*args,**kwargs)
                    connection.send(pickle.dumps(r))
                except Exception as e:
                    connection.send(pickle.dumps(e))
        except EOFError:
             pass

To use this handler, you need to add it into a messaging server. There are many possible
choices, but the multiprocessing library provides a simple option. Here is an example
RPC server:

from multiprocessing.connection import Listener
from threading import Thread

def rpc_server(handler, address, authkey):
    sock = Listener(address, authkey=authkey)
    while True:
        client = sock.accept()
        t = Thread(target=handler.handle_connection, args=(client,))
        t.daemon = True
        t.start()

# Some remote functions
def add(x, y):
    return x + y

def sub(x, y):
    return x - y

# Register with a handler
handler = RPCHandler()
handler.register_function(add)
handler.register_function(sub)

# Run the server
rpc_server(handler, ('localhost', 17000), authkey=b'peekaboo')

To access the server from a remote client, you need to create a corresponding RPC proxy
class that forwards requests. For example:

import pickle

class RPCProxy:
    def __init__(self, connection):
        self._connection = connection
    def __getattr__(self, name):
        def do_rpc(*args, **kwargs):
            self._connection.send(pickle.dumps((name, args, kwargs)))
            result = pickle.loads(self._connection.recv())
            if isinstance(result, Exception):
                raise result
            return result
        return do_rpc

To use the proxy, you wrap it around a connection to the server. For example:

>>> from multiprocessing.connection import Client
>>> c = Client(('localhost', 17000), authkey=b'peekaboo')
>>> proxy = RPCProxy(c)
>>> proxy.add(2, 3)

5
>>> proxy.sub(2, 3)
-1
>>> proxy.sub([1, 2], 4)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "rpcserver.py", line 37, in do_rpc
    raise result
TypeError: unsupported operand type(s) for -: 'list' and 'int'
>>>

It should be noted that many messaging layers (such as multiprocessing) already se‐
rialize data using pickle. If this is the case, the pickle.dumps() and pickle.loads()
calls can be eliminated.

|

----------
讨论
----------
The general idea of the RPCHandler and RPCProxy classes is relatively simple. If a client
wants to call a remote function, such as foo(1, 2, z=3), the proxy class creates a tuple
('foo', (1, 2), {'z': 3}) that contains the function name and arguments. This
tuple is pickled and sent over the connection. This is performed in the do_rpc() closure
that’s returned by the  __getattr__() method of  RPCProxy. The server receives and
unpickles the message, looks up the function name to see if it’s registered, and executes
it with the given arguments. The result (or exception) is then pickled and sent back.
As shown, the example relies on multiprocessing for communication. However, this
approach could be made to work with just about any other messaging system. For ex‐
ample, if you want to implement RPC over ZeroMQ, just replace the connection objects
with an appropriate ZeroMQ socket object.
Given the reliance on pickle, security is a major concern (because a clever hacker can
create messages that make arbitrary functions execute during unpickling). In particular,
you should never allow RPC from untrusted or unauthenticated clients. In particular,
you definitely don’t want to allow access from just any machine on the Internet—this
should really only be used internally, behind a firewall, and not exposed to the rest of
the world.
As an alternative to pickle, you might consider the use of JSON, XML, or some other
data encoding for serialization. For example, this recipe is fairly easy to adapt to JSON
encoding 
if  you  simply  replace  pickle.loads()  and  pickle.dumps()  with
json.loads() and json.dumps(). For example:

# jsonrpcserver.py
import json

class RPCHandler:
    def __init__(self):
        self._functions = { }

    def register_function(self, func):
        self._functions[func.__name__] = func

    def handle_connection(self, connection):
        try:
            while True:
                # Receive a message
                func_name, args, kwargs = json.loads(connection.recv())
                # Run the RPC and send a response
                try:
                    r = self._functions[func_name](*args,**kwargs)
                    connection.send(json.dumps(r))
                except Exception as e:
                    connection.send(json.dumps(str(e)))
        except EOFError:
             pass

# jsonrpcclient.py
import json

class RPCProxy:
    def __init__(self, connection):
        self._connection = connection
    def __getattr__(self, name):
        def do_rpc(*args, **kwargs):
            self._connection.send(json.dumps((name, args, kwargs)))
            result = json.loads(self._connection.recv())
            return result
        return do_rpc

One complicated factor in implementing RPC is how to handle exceptions. At the very
least, the server shouldn’t crash if an exception is raised by a method. However, the
means by which the exception gets reported back to the client requires some study. If
you’re using  pickle, exception instances can often be serialized and reraised in the
client. If you’re using some other protocol, you might have to think of an alternative
approach. At the very least, you would probably want to return the exception string in
the response. This is the approach taken in the JSON example.
For another example of an RPC implementation, it can be useful to look at the imple‐
mentation of the SimpleXMLRPCServer and ServerProxy classes used in XML-RPC, as
described in Recipe 11.6.
