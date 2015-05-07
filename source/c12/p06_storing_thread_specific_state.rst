============================
12.6 保存线程的状态信息
============================

----------
问题
----------
You need to store state that’s specific to the currently executing thread and not visible
to other threads.

Solution
Sometimes in multithreaded programs, you need to store data that is only specific to
the currently executing thread. To do this, create a thread-local storage object using
threading.local(). Attributes stored and read on this object are only visible to the
executing thread and no others.
As an interesting practical example of using thread-local storage, consider the LazyCon
nection context-manager class that was first defined in Recipe 8.3. Here is a slightly
modified version that safely works with multiple threads:

from socket import socket, AF_INET, SOCK_STREAM
import threading

class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.local = threading.local()

    def __enter__(self):
        if hasattr(self.local, 'sock'):
            raise RuntimeError('Already connected')
        self.local.sock = socket(self.family, self.type)
        self.local.sock.connect(self.address)
        return self.local.sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.local.sock.close()
        del self.local.sock

In this code, carefully observe the use of the self.local attribute. It is initialized as an
instance of  threading.local(). The other methods then manipulate a socket that’s
stored as self.local.sock. This is enough to make it possible to safely use an instance
of LazyConnection in multiple threads. For example:

from functools import partial
def test(conn):
    with conn as s:
        s.send(b'GET /index.html HTTP/1.0\r\n')
        s.send(b'Host: www.python.org\r\n')

        s.send(b'\r\n')
        resp = b''.join(iter(partial(s.recv, 8192), b''))

    print('Got {} bytes'.format(len(resp)))

if __name__ == '__main__':
    conn = LazyConnection(('www.python.org', 80))

    t1 = threading.Thread(target=test, args=(conn,))
    t2 = threading.Thread(target=test, args=(conn,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

The reason it works is that each thread actually creates its own dedicated socket con‐
nection (stored as self.local.sock). Thus, when the different threads perform socket
operations, they don’t interfere with one another as they are being performed on dif‐
ferent sockets.

Discussion
Creating and manipulating thread-specific state is not a problem that often arises in
most programs. However, when it does, it commonly involves situations where an object
being used by multiple threads needs to manipulate some kind of dedicated system
resource, such as a socket or file. You can’t just have a single socket object shared by
everyone because chaos would ensue if multiple threads ever started reading and writing
on it at the same time. Thread-local storage fixes this by making such resources only
visible in the thread where they’re being used.
In this recipe, the use of threading.local() makes the LazyConnection class support
one connection per thread, as opposed to one connection for the entire process. It’s a
subtle but interesting distinction.
Under the covers, an instance of  threading.local() maintains a separate instance
dictionary for each thread. All of the usual instance operations of getting, setting, and
deleting values just manipulate the per-thread dictionary. The fact that each thread uses
a separate dictionary is what provides the isolation of data.
