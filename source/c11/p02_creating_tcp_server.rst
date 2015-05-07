============================
11.2 创建TCP服务器
============================

----------
问题
----------
You want to implement a server that communicates with clients using the TCP Internet
protocol.

|

----------
解决方案
----------
An easy way to create a TCP server is to use the socketserver library. For example,
here is a simple echo server:

from socketserver import BaseRequestHandler, TCPServer

class EchoHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        while True:

            msg = self.request.recv(8192)
            if not msg:
                break
            self.request.send(msg)

if __name__ == '__main__':
    serv = TCPServer(('', 20000), EchoHandler)
    serv.serve_forever()

In this code, you define a special handler class that implements a handle() method for
servicing client connections. The request attribute is the underlying client socket and
client_address has client address.
To test the server, run it and then open a separate Python process that connects to it:

>>> from socket import socket, AF_INET, SOCK_STREAM
>>> s = socket(AF_INET, SOCK_STREAM)
>>> s.connect(('localhost', 20000))
>>> s.send(b'Hello')
5
>>> s.recv(8192)
b'Hello'
>>>

In many cases, it may be easier to define a slightly different kind of handler. Here is an
example that uses the StreamRequestHandler base class to put a file-like interface on
the underlying socket:

from socketserver import StreamRequestHandler, TCPServer

class EchoHandler(StreamRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        # self.rfile is a file-like object for reading
        for line in self.rfile:
            # self.wfile is a file-like object for writing
            self.wfile.write(line)

if __name__ == '__main__':
    serv = TCPServer(('', 20000), EchoHandler)
    serv.serve_forever()

|

----------
讨论
----------
socketserver  makes  it  relatively  easy  to  create  simple  TCP  servers.  However,  you
should be aware that, by default, the servers are single threaded and can only serve one
client at a time. If you want to handle multiple clients, either instantiate a ForkingTCP
Server or ThreadingTCPServer object instead. For example:

from socketserver import ThreadingTCPServer
...

if __name__ == '__main__':
    serv = ThreadingTCPServer(('', 20000), EchoHandler)
    serv.serve_forever()

One issue with forking and threaded servers is that they spawn a new process or thread
on each client connection. There is no upper bound on the number of allowed clients,
so a malicious hacker could potentially launch a large number of simultaneous con‐
nections in an effort to make your server explode.
If this is a concern, you can create a pre-allocated pool of worker threads or processes.
To do this, you create an instance of a normal nonthreaded server, but then launch the
serve_forever() method in a pool of multiple threads. For example:

...
if __name__ == '__main__':
    from threading import Thread
    NWORKERS = 16
    serv = TCPServer(('', 20000), EchoHandler)
    for n in range(NWORKERS):
        t = Thread(target=serv.serve_forever)
        t.daemon = True
        t.start()
    serv.serve_forever()

Normally, a TCPServer binds and activates the underlying socket upon instantiation.
However, sometimes you might want to adjust the underlying socket by setting options.
To do this, supply the bind_and_activate=False argument, like this:

if __name__ == '__main__':
    serv = TCPServer(('', 20000), EchoHandler, bind_and_activate=False)
    # Set up various socket options
    serv.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # Bind and activate
    serv.server_bind()
    serv.server_activate()
    serv.serve_forever()

The socket option shown is actually a very common setting that allows the server to
rebind to a previously used port number. It’s actually so common that it’s a class variable
that can be set on TCPServer. Set it before instantiating the server, as shown in this
example:

...
if __name__ == '__main__':
    TCPServer.allow_reuse_address = True
    serv = TCPServer(('', 20000), EchoHandler)
    serv.serve_forever()

In the solution, two different handler base classes were shown (BaseRequestHandler
and StreamRequestHandler). The StreamRequestHandler class is actually a bit more

flexible, and supports some features that can be enabled through the specification of
additional class variables. For example:

import socket

class EchoHandler(StreamRequestHandler):
    # Optional settings (defaults shown)
    timeout = 5                      # Timeout on all socket operations
    rbufsize = -1                    # Read buffer size
    wbufsize = 0                     # Write buffer size
    disable_nagle_algorithm = False  # Sets TCP_NODELAY socket option
    def handle(self):
        print('Got connection from', self.client_address)
        try:
            for line in self.rfile:
                # self.wfile is a file-like object for writing
                self.wfile.write(line)
        except socket.timeout:
            print('Timed out!')

Finally, it should be noted that most of Python’s higher-level networking modules (e.g.,
HTTP, XML-RPC, etc.) are built on top of the socketserver functionality. That said,
it is also not difficult to implement servers directly using the socket library as well. Here
is a simple example of directly programming a server with Sockets:

from socket import socket, AF_INET, SOCK_STREAM

def echo_handler(address, client_sock):
    print('Got connection from {}'.format(address))
    while True:
        msg = client_sock.recv(8192)
        if not msg:
            break
        client_sock.sendall(msg)
    client_sock.close()

def echo_server(address, backlog=5):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(backlog)
    while True:
        client_sock, client_addr = sock.accept()
        echo_handler(client_addr, client_sock)

if __name__ == '__main__':
    echo_server(('', 20000))

