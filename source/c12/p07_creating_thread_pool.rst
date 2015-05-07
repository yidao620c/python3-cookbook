============================
12.7 创建一个线程池
============================

----------
问题
----------
You want to create a pool of worker threads for serving clients or performing other kinds
of work.

|

----------
解决方案
----------
The concurrent.futures library has a ThreadPoolExecutor class that can be used for
this purpose. Here is an example of a simple TCP server that uses a thread-pool to serve
clients:

from socket import AF_INET, SOCK_STREAM, socket
from concurrent.futures import ThreadPoolExecutor

def echo_client(sock, client_addr):
    '''
    Handle a client connection
    '''
    print('Got connection from', client_addr)
    while True:
        msg = sock.recv(65536)
        if not msg:
            break
        sock.sendall(msg)
    print('Client closed connection')
    sock.close()

def echo_server(addr):
    pool = ThreadPoolExecutor(128)
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(addr)
    sock.listen(5)
    while True:
        client_sock, client_addr = sock.accept()
        pool.submit(echo_client, client_sock, client_addr)

echo_server(('',15000))

If you want to manually create your own thread pool, it’s usually easy enough to do it
using a Queue. Here is a slightly different, but manual implementation of the same code:

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from queue import Queue

def echo_client(q):
    '''
    Handle a client connection
    '''
    sock, client_addr = q.get()
    print('Got connection from', client_addr)
    while True:
        msg = sock.recv(65536)
        if not msg:
            break
        sock.sendall(msg)
    print('Client closed connection')

    sock.close()

def echo_server(addr, nworkers):
    # Launch the client workers
    q = Queue()
    for n in range(nworkers):
        t = Thread(target=echo_client, args=(q,))
        t.daemon = True
        t.start()

    # Run the server
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(addr)
    sock.listen(5)
    while True:
        client_sock, client_addr = sock.accept()
        q.put((client_sock, client_addr))

echo_server(('',15000), 128)

One advantage of using ThreadPoolExecutor over a manual implementation is that it
makes it easier for the submitter to receive results from the called function. For example,
you could write code like this:

from concurrent.futures import ThreadPoolExecutor
import urllib.request

def fetch_url(url):
    u = urllib.request.urlopen(url)
    data = u.read()
    return data

pool = ThreadPoolExecutor(10)
# Submit work to the pool
a = pool.submit(fetch_url, 'http://www.python.org')
b = pool.submit(fetch_url, 'http://www.pypy.org')

# Get the results back
x = a.result()
y = b.result()

The result objects in the example handle all of the blocking and coordination needed
to get data back from the worker thread. Specifically, the operation a.result() blocks
until the corresponding function has been executed by the pool and returned a value.

|

----------
讨论
----------
Generally, you should avoid writing programs that allow unlimited growth in the num‐
ber of threads. For example, take a look at the following server:

from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM

def echo_client(sock, client_addr):
    '''
    Handle a client connection
    '''
    print('Got connection from', client_addr)
    while True:
        msg = sock.recv(65536)
        if not msg:
            break
        sock.sendall(msg)
    print('Client closed connection')
    sock.close()

def echo_server(addr, nworkers):
    # Run the server
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(addr)
    sock.listen(5)
    while True:
        client_sock, client_addr = sock.accept()
        t = Thread(target=echo_client, args=(client_sock, client_addr))
        t.daemon = True
        t.start()

echo_server(('',15000))

Although this works, it doesn’t prevent some asynchronous hipster from launching an
attack on the server that makes it create so many threads that your program runs out
of resources and crashes (thus further demonstrating the “evils” of using threads). By
using a pre-initialized thread pool, you can carefully put an upper limit on the amount
of supported concurrency.
You might be concerned with the effect of creating a large number of threads. However,
modern  systems  should  have  no  trouble  creating  pools  of  a  few  thousand  threads.
Moreover, having a thousand threads just sitting around waiting for work isn’t going to
have much, if any, impact on the performance of other code (a sleeping thread does just
that—nothing at all). Of course, if all of those threads wake up at the same time and
start hammering on the CPU, that’s a different story—especially in light of the Global
Interpreter Lock (GIL). Generally, you only want to use thread pools for I/O-bound
processing.
One possible concern with creating large thread pools might be memory use. For ex‐
ample, if you create 2,000 threads on OS X, the system shows the Python process using
up more than 9 GB of virtual memory. However, this is actually somewhat misleading.
When creating a thread, the operating system reserves a region of virtual memory to
hold the thread’s execution stack (often as large as 8 MB). Only a small fragment of this
memory is actually mapped to real memory, though. Thus, if you look a bit closer, you
might find the Python process is using far less real memory (e.g., for 2,000 threads, only

70 MB of real memory is used, not 9 GB). If the size of the virtual memory is a concern,
you can dial it down using the threading.stack_size() function. For example:

import threading
threading.stack_size(65536)

If you add this call and repeat the experiment of creating 2,000 threads, you’ll find that
the Python process is now only using about 210 MB of virtual memory, although the
amount of real memory in use remains about the same. Note that the thread stack size
must be at least 32,768 bytes, and is usually restricted to be a multiple of the system
memory page size (4096, 8192, etc.).
