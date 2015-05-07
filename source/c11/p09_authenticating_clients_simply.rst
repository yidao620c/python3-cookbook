===============================
11.9 简单的客户端认证
===============================

----------
问题
----------
You want a simple way to authenticate the clients connecting to servers in a distributed
system, but don’t need the complexity of something like SSL.

Solution
Simple but effective authentication can be performed by implementing a connection
handshake using the hmac module. Here is sample code:

import hmac
import os

def client_authenticate(connection, secret_key):
    '''
    Authenticate client to a remote service.
    connection represents a network connection.
    secret_key is a key known only to both client/server.
    '''
    message = connection.recv(32)
    hash = hmac.new(secret_key, message)
    digest = hash.digest()
    connection.send(digest)

def server_authenticate(connection, secret_key):
    '''
    Request client authentication.
    '''
    message = os.urandom(32)
    connection.send(message)
    hash = hmac.new(secret_key, message)
    digest = hash.digest()
    response = connection.recv(len(digest))
    return hmac.compare_digest(digest,response)

The general idea is that upon connection, the server presents the client with a message
of random bytes (returned by os.urandom(), in this case). The client and server both
compute a cryptographic hash of the random data using hmac and a secret key known
only to both ends. The client sends its computed digest back to the server, where it is
compared and used to decide whether or not to accept or reject the connection.
Comparison  of  resulting  digests  should  be  performed  using  the  hmac.compare_di
gest() function. This function has been written in a way that avoids timing-analysis-
based attacks and should be used instead of a normal comparison operator (==).
To use these functions, you would incorporate them into existing networking or mes‐
saging code. For example, with sockets, the server code might look something like this:

from socket import socket, AF_INET, SOCK_STREAM

secret_key = b'peekaboo'
def echo_handler(client_sock):
    if not server_authenticate(client_sock, secret_key):
        client_sock.close()
        return
    while True:

        msg = client_sock.recv(8192)
        if not msg:
            break
        client_sock.sendall(msg)

def echo_server(address):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    while True:
        c,a = s.accept()
        echo_handler(c)

echo_server(('', 18000))

Within a client, you would do this:

from socket import socket, AF_INET, SOCK_STREAM

secret_key = b'peekaboo'

s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 18000))
client_authenticate(s, secret_key)
s.send(b'Hello World')
resp = s.recv(1024)
...

Discussion
A common use of hmac authentication is in internal messaging systems and interprocess
communication. For example, if you are writing a system that involves multiple pro‐
cesses communicating across a cluster of machines, you can use this approach to make
sure that only allowed processes are allowed to connect to one another. In fact, HMAC-
based authentication is used internally by the multiprocessing library when it sets up
communication with subprocesses.
It’s important to stress that authenticating a connection is not the same as encryption.
Subsequent communication on an authenticated connection is sent in the clear, and
would be visible to anyone inclined to sniff the traffic (although the secret key known
to both sides is never transmitted).
The authentication algorithm used by hmac is based on cryptographic hashing functions,
such as MD5 and SHA-1, and is described in detail in IETF RFC 2104. 

