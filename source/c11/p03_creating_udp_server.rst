============================
11.3 创建UDP服务器
============================

----------
问题
----------
You want to implement a server that communicates with clients using the UDP Internet
protocol.

Solution
As with TCP, UDP servers are also easy to create using the socketserver library. For
example, here is a simple time server:

from socketserver import BaseRequestHandler, UDPServer
import time

class TimeHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        # Get message and client socket
        msg, sock = self.request
        resp = time.ctime()
        sock.sendto(resp.encode('ascii'), self.client_address)

if __name__ == '__main__':
    serv = UDPServer(('', 20000), TimeHandler)
    serv.serve_forever()

As before, you define a special handler class that implements a handle() method for
servicing client connections. The request attribute is a tuple that contains the incoming
datagram and underlying socket object for the server. The client_address contains
the client address.
To test the server, run it and then open a separate Python process that sends messages
to it:

>>> from socket import socket, AF_INET, SOCK_DGRAM
>>> s = socket(AF_INET, SOCK_DGRAM)
>>> s.sendto(b'', ('localhost', 20000))
0
>>> s.recvfrom(8192)
(b'Wed Aug 15 20:35:08 2012', ('127.0.0.1', 20000))
>>>

Discussion
A typical UDP server receives an incoming datagram (message) along with a client
address. If the server is to respond, it sends a datagram back to the client. For trans‐
mission of datagrams, you should use the  sendto() and  recvfrom() methods of a

socket. Although the traditional send() and recv() methods also might work, the for‐
mer two methods are more commonly used with UDP communication.
Given that there is no underlying connection, UDP servers are often much easier to
write than a TCP server. However, UDP is also inherently unreliable (e.g., no “connec‐
tion” is established and messages might be lost). Thus, it would be up to you to figure
out how to deal with lost messages. That’s a topic beyond the scope of this book, but
typically you might need to introduce sequence numbers, retries, timeouts, and other
mechanisms to ensure reliability if it matters for your application. UDP is often used in
cases where the requirement of reliable delivery can be relaxed. For instance, in real-
time applications such as multimedia streaming and games where there is simply no
option to go back in time and recover a lost packet (the program simply skips it and
keeps moving forward).
The UDPServer class is single threaded, which means that only one request can be serv‐
iced at a time. In practice, this is less of an issue with UDP than with TCP connections.
However, should you want concurrent operation, instantiate a ForkingUDPServer or
ThreadingUDPServer object instead:

from socketserver import ThreadingUDPServer
...
if __name__ == '__main__':
    serv = ThreadingUDPServer(('',20000), TimeHandler)
    serv.serve_forever()

Implementing  a  UDP  server  directly  using  sockets  is  also  not  difficult.  Here  is  an
example:

from socket import socket, AF_INET, SOCK_DGRAM
import time

def time_server(address):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(address)
    while True:
        msg, addr = sock.recvfrom(8192)
        print('Got message from', addr)
        resp = time.ctime()
        sock.sendto(resp.encode('ascii'), addr)

if __name__ == '__main__':
    time_server(('', 20000))

