==============================
11.11 进程间传递Socket文件描述符
==============================

----------
问题
----------
You have multiple Python interpreter processes running and you want to pass an open
file descriptor from one interpreter to the other. For instance, perhaps there is a server
process that is responsible for receiving connections, but the actual servicing of clients
is to be handled by a different interpreter.

|

----------
解决方案
----------
To pass a file descriptor between processes, you first need to connect the processes
together. On Unix machines, you might use a Unix domain socket, whereas on Win‐
dows,  you  could  use  a  named  pipe.  However,  rather  than  deal  with  such  low-level
mechanics,  it  is  often  easier  to  use  the  multiprocessing  module  to  set  up  such  a
connection.

Once a connection is established, you can use the send_handle() and recv_handle()
functions in multiprocessing.reduction to send file descriptors between processes.
The following example illustrates the basics:

import multiprocessing
from multiprocessing.reduction import recv_handle, send_handle
import socket

def worker(in_p, out_p):
    out_p.close()
    while True:
        fd = recv_handle(in_p)
        print('CHILD: GOT FD', fd)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, fileno=fd) as s:
            while True:
                msg = s.recv(1024)
                if not msg:
                    break
                print('CHILD: RECV {!r}'.format(msg))
                s.send(msg)

def server(address, in_p, out_p, worker_pid):
    in_p.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    s.bind(address)
    s.listen(1)
    while True:
        client, addr = s.accept()
        print('SERVER: Got connection from', addr)
        send_handle(out_p, client.fileno(), worker_pid)
        client.close()

if __name__ == '__main__':
    c1, c2 = multiprocessing.Pipe()
    worker_p = multiprocessing.Process(target=worker, args=(c1,c2))
    worker_p.start()

    server_p = multiprocessing.Process(target=server,
                  args=(('', 15000), c1, c2, worker_p.pid))
    server_p.start()

    c1.close()
    c2.close()

In this example, two processes are spawned and connected by a multiprocessing Pipe
object. The server process opens a socket and waits for client connections. The worker
process merely waits to receive a file descriptor on the pipe using recv_handle(). When
the server receives a connection, it sends the resulting socket file descriptor to the worker

using send_handle(). The worker takes over the socket and echoes data back to the
client until the connection is closed.
If you connect to the running server using Telnet or a similar tool, here is an example
of what you might see:

    bash % python3 passfd.py
    SERVER: Got connection from ('127.0.0.1', 55543)
    CHILD: GOT FD 7
    CHILD: RECV b'Hello\r\n'
    CHILD: RECV b'World\r\n'

The most important part of this example is the fact that the client socket accepted in the
server is actually serviced by a completely different process. The server merely hands it
off, closes it, and waits for the next connection.

|

----------
讨论
----------
Passing file descriptors between processes is something that many programmers don’t
even realize is possible. However, it can sometimes be a useful tool in building scalable
systems. For example, on a multicore machine, you could have multiple instances of the
Python interpreter and use file descriptor passing to more evenly balance the number
of clients being handled by each interpreter.
The send_handle() and recv_handle() functions shown in the solution really only
work with multiprocessing connections. Instead of using a pipe, you can connect in‐
terpreters as shown in Recipe 11.7, and it will work as long as you use UNIX domain
sockets or Windows pipes. For example, you could implement the server and worker
as completely separate programs to be started separately. Here is the implementation of
the server:

# servermp.py
from multiprocessing.connection import Listener
from multiprocessing.reduction import send_handle
import socket

def server(work_address, port):
    # Wait for the worker to connect
    work_serv = Listener(work_address, authkey=b'peekaboo')
    worker = work_serv.accept()
    worker_pid = worker.recv()

    # Now run a TCP/IP server and send clients to worker
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    s.bind(('', port))
    s.listen(1)
    while True:
        client, addr = s.accept()
        print('SERVER: Got connection from', addr)

        send_handle(worker, client.fileno(), worker_pid)
        client.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('Usage: server.py server_address port', file=sys.stderr)
        raise SystemExit(1)

    server(sys.argv[1], int(sys.argv[2]))

To run this server, you would run a command such as python3 servermp.py /tmp/
servconn 15000. Here is the corresponding client code:

# workermp.py

from multiprocessing.connection import Client
from multiprocessing.reduction import recv_handle
import os
from socket import socket, AF_INET, SOCK_STREAM

def worker(server_address):
    serv = Client(server_address, authkey=b'peekaboo')
    serv.send(os.getpid())
    while True:
        fd = recv_handle(serv)
        print('WORKER: GOT FD', fd)
        with socket(AF_INET, SOCK_STREAM, fileno=fd) as client:
            while True:
                msg = client.recv(1024)
                if not msg:
                    break
                print('WORKER: RECV {!r}'.format(msg))
                client.send(msg)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('Usage: worker.py server_address', file=sys.stderr)
        raise SystemExit(1)

    worker(sys.argv[1])

To run the worker, you would type python3 workermp.py /tmp/servconn. The result‐
ing operation should be exactly the same as the example that used Pipe().
Under the covers, file descriptor passing involves creating a UNIX domain socket and
the sendmsg() method of sockets. Since this technique is not widely known, here is a
different implementation of the server that shows how to pass descriptors using sockets:

# server.py
import socket

import struct

def send_fd(sock, fd):
    '''
    Send a single file descriptor.
    '''
    sock.sendmsg([b'x'],
                 [(socket.SOL_SOCKET, socket.SCM_RIGHTS, struct.pack('i', fd))])
    ack = sock.recv(2)
    assert ack == b'OK'

def server(work_address, port):
    # Wait for the worker to connect
    work_serv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    work_serv.bind(work_address)
    work_serv.listen(1)
    worker, addr = work_serv.accept()

    # Now run a TCP/IP server and send clients to worker
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    s.bind(('',port))
    s.listen(1)
    while True:
        client, addr = s.accept()
        print('SERVER: Got connection from', addr)
        send_fd(worker, client.fileno())
        client.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('Usage: server.py server_address port', file=sys.stderr)
        raise SystemExit(1)

    server(sys.argv[1], int(sys.argv[2]))

Here is an implementation of the worker using sockets:

# worker.py
import socket
import struct

def recv_fd(sock):
    '''
    Receive a single file descriptor
    '''
    msg, ancdata, flags, addr = sock.recvmsg(1,
                                     socket.CMSG_LEN(struct.calcsize('i')))

    cmsg_level, cmsg_type, cmsg_data = ancdata[0]
    assert cmsg_level == socket.SOL_SOCKET and cmsg_type == socket.SCM_RIGHTS
    sock.sendall(b'OK')

    return struct.unpack('i', cmsg_data)[0]

def worker(server_address):
    serv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    serv.connect(server_address)
    while True:
        fd = recv_fd(serv)
        print('WORKER: GOT FD', fd)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, fileno=fd) as client:
            while True:
                msg = client.recv(1024)
                if not msg:
                    break
                print('WORKER: RECV {!r}'.format(msg))
                client.send(msg)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('Usage: worker.py server_address', file=sys.stderr)
        raise SystemExit(1)

    worker(sys.argv[1])

If you are going to use file-descriptor passing in your program, it is advisable to read
more about it in an advanced text, such as Unix Network Programming by W. Richard
Stevens  (Prentice  Hall,  1990).  Passing  file  descriptors  on  Windows  uses  a  different
technique than Unix (not shown). For that platform, it is advisable to study the source
code to multiprocessing.reduction in close detail to see how it works.
