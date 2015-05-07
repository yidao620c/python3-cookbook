==============================
11.13 发送与接收大型数组
==============================

----------
问题
----------
You want to send and receive large arrays of contiguous data across a network connec‐
tion, making as few copies of the data as possible.

|

----------
解决方案
----------
The following functions utilize memoryviews to send and receive large arrays:

# zerocopy.py

def send_from(arr, dest):
    view = memoryview(arr).cast('B')
    while len(view):
        nsent = dest.send(view)
        view = view[nsent:]

def recv_into(arr, source):
    view = memoryview(arr).cast('B')
    while len(view):
        nrecv = source.recv_into(view)
        view = view[nrecv:]

To test the program, first create a server and client program connected over a socket.
In the server:

>>> from socket import *
>>> s = socket(AF_INET, SOCK_STREAM)
>>> s.bind(('', 25000))
>>> s.listen(1)
>>> c,a = s.accept()
>>>

In the client (in a separate interpreter):

>>> from socket import *
>>> c = socket(AF_INET, SOCK_STREAM)
>>> c.connect(('localhost', 25000))
>>>

Now, the whole idea of this recipe is that you can blast a huge array through the con‐
nection. In this case, arrays might be created by the array module or perhaps numpy.
For example:
# Server
>>> import numpy
>>> a = numpy.arange(0.0, 50000000.0)
>>> send_from(a, c)
>>>

# Client
>>> import numpy
>>> a = numpy.zeros(shape=50000000, dtype=float)
>>> a[0:10]
array([ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.])
>>> recv_into(a, c)
>>> a[0:10]
array([ 0.,  1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9.])
>>>

|

----------
讨论
----------
In data-intensive distributed computing and parallel programming applications, it’s not
uncommon to write programs that need to send/receive large chunks of data. However,
to do this, you somehow need to reduce the data down to raw bytes for use with low-
level network functions. You may also need to slice the data into chunks, since most
network-related functions aren’t able to send or receive huge blocks of data entirely all
at once.
One approach is to serialize the data in some way—possibly by converting into a byte
string. However, this usually ends up making a copy of the data. Even if you do this
piecemeal, your code still ends up making a lot of little copies.

This recipe gets around this by playing a sneaky trick with memoryviews. Essentially, a
memoryview is an overlay of an existing array. Not only that, memoryviews can be cast
to different types to allow interpretation of the data in a different manner. This is the
purpose of the following statement:
view = memoryview(arr).cast('B')

It takes an array arr and casts into a memoryview of unsigned bytes.
In this form, the view can be passed to socket-related functions, such as sock.send()
or send.recv_into(). Under the covers, those methods are able to work directly with
the  memory  region.  For  example,  sock.send()  sends  data  directly  from  memory
without a copy. send.recv_into() uses the memoryview as the input buffer for the
receive operation.
The remaining complication is the fact that the socket functions may only work with
partial data. In general, it will take many different send() and recv_into() calls to
transmit the entire array. Not to worry. After each operation, the view is sliced by the
number of sent or received bytes to produce a new view. The new view is also a memory
overlay. Thus, no copies are made.
One issue here is that the receiver has to know in advance how much data will be sent
so that it can either preallocate an array or verify that it can receive the data into an
existing array. If this is a problem, the sender could always arrange to send the size first,
followed by the array data.


