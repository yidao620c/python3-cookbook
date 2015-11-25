===============================
11.10 在网络服务中加入SSL
===============================

----------
问题
----------
你想实现一个基于sockets的网络服务，客户端和服务器通过SSL协议认证并加密传输的数据。

|

----------
解决方案
----------
``ssl`` 模块能为底层socket连接添加SSL的支持。
``ssl.wrap_socket()`` 函数接受一个已存在的socket作为参数并使用SSL层来包装它。
例如，下面是一个简单的应答服务器，能在服务器端为所有客户端连接做认证。

.. code-block:: python

    from socket import socket, AF_INET, SOCK_STREAM
    import ssl

    KEYFILE = 'server_key.pem'   # Private key of the server
    CERTFILE = 'server_cert.pem' # Server certificate (given to client)

    def echo_client(s):
        while True:
            data = s.recv(8192)
            if data == b'':
                break
            s.send(data)
        s.close()
        print('Connection closed')

    def echo_server(address):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(address)
        s.listen(1)

        # Wrap with an SSL layer requiring client certs
        s_ssl = ssl.wrap_socket(s,
                                keyfile=KEYFILE,
                                certfile=CERTFILE,
                                server_side=True
                                )
        # Wait for connections
        while True:
            try:
                c,a = s_ssl.accept()
                print('Got connection', c, a)
                echo_client(c)
            except Exception as e:
                print('{}: {}'.format(e.__class__.__name__, e))

    echo_server(('', 20000))

下面我们演示一个客户端连接服务器的交互例子。客户端会请求服务器来认证并确认连接：

.. code-block:: python

    >>> from socket import socket, AF_INET, SOCK_STREAM
    >>> import ssl
    >>> s = socket(AF_INET, SOCK_STREAM)
    >>> s_ssl = ssl.wrap_socket(s,
                    cert_reqs=ssl.CERT_REQUIRED,
                    ca_certs = 'server_cert.pem')
    >>> s_ssl.connect(('localhost', 20000))
    >>> s_ssl.send(b'Hello World?')
    12
    >>> s_ssl.recv(8192)
    b'Hello World?'
    >>>

这种直接处理底层socket方式有个问题就是它不能很好的跟标准库中已存在的网络服务兼容。
例如，绝大部分服务器代码（HTTP、XML-RPC等）实际上是基于 ``socketserver`` 库的。
客户端代码在一个较高层上实现。我们需要另外一种稍微不同的方式来将SSL添加到已存在的服务中：

首先，对于服务器而言，可以通过像下面这样使用一个mixin类来添加SSL：

.. code-block:: python

        import ssl

        class SSLMixin:
        '''
        Mixin class that adds support for SSL to existing servers based
        on the socketserver module.
        '''
        def __init__(self, *args,
                     keyfile=None, certfile=None, ca_certs=None,
                     cert_reqs=ssl.NONE,
                     **kwargs):
            self._keyfile = keyfile
            self._certfile = certfile
            self._ca_certs = ca_certs
            self._cert_reqs = cert_reqs
            super().__init__(*args, **kwargs)

        def get_request(self):
            client, addr = super().get_request()
            client_ssl = ssl.wrap_socket(client,
                                         keyfile = self._keyfile,
                                         certfile = self._certfile,
                                         ca_certs = self._ca_certs,
                                         cert_reqs = self._cert_reqs,
                                         server_side = True)
            return client_ssl, addr

为了使用这个mixin类，你可以将它跟其他服务器类混合。例如，下面是定义一个基于SSL的XML-RPC服务器例子：

.. code-block:: python

    # XML-RPC server with SSL

    from xmlrpc.server import SimpleXMLRPCServer

    class SSLSimpleXMLRPCServer(SSLMixin, SimpleXMLRPCServer):
        pass

    Here's the XML-RPC server from Recipe 11.6 modified only slightly to use SSL:

    import ssl
    from xmlrpc.server import SimpleXMLRPCServer
    from sslmixin import SSLMixin

    class SSLSimpleXMLRPCServer(SSLMixin, SimpleXMLRPCServer):
        pass

    class KeyValueServer:
        _rpc_methods_ = ['get', 'set', 'delete', 'exists', 'keys']
        def __init__(self, *args, **kwargs):
            self._data = {}
            self._serv = SSLSimpleXMLRPCServer(*args, allow_none=True, **kwargs)
            for name in self._rpc_methods_:
                self._serv.register_function(getattr(self, name))

        def get(self, name):
            return self._data[name]

        def set(self, name, value):
            self._data[name] = value

        def delete(self, name):
            del self._data[name]

        def exists(self, name):
            return name in self._data

        def keys(self):
            return list(self._data)

        def serve_forever(self):
            self._serv.serve_forever()

    if __name__ == '__main__':
        KEYFILE='server_key.pem'    # Private key of the server
        CERTFILE='server_cert.pem'  # Server certificate
        kvserv = KeyValueServer(('', 15000),
                                keyfile=KEYFILE,
                                certfile=CERTFILE),
        kvserv.serve_forever()

使用这个服务器时，你可以使用普通的 ``xmlrpc.client`` 模块来连接它。
只需要在URL中指定 ``https:`` 即可，例如：

.. code-block:: python

    >>> from xmlrpc.client import ServerProxy
    >>> s = ServerProxy('https://localhost:15000', allow_none=True)
    >>> s.set('foo','bar')
    >>> s.set('spam', [1, 2, 3])
    >>> s.keys()
    ['spam', 'foo']
    >>> s.get('foo')
    'bar'
    >>> s.get('spam')
    [1, 2, 3]
    >>> s.delete('spam')
    >>> s.exists('spam')
    False
    >>>

对于SSL客户端来讲一个比较复杂的问题是如何确认服务器证书或为服务器提供客户端认证（比如客户端证书）。
不幸的是，暂时还没有一个标准方法来解决这个问题，需要自己去研究。
不过，下面给出一个例子，用来建立一个安全的XML-RPC连接来确认服务器证书：

.. code-block:: python

    from xmlrpc.client import SafeTransport, ServerProxy
    import ssl

    class VerifyCertSafeTransport(SafeTransport):
        def __init__(self, cafile, certfile=None, keyfile=None):
            SafeTransport.__init__(self)
            self._ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            self._ssl_context.load_verify_locations(cafile)
            if cert:
                self._ssl_context.load_cert_chain(certfile, keyfile)
            self._ssl_context.verify_mode = ssl.CERT_REQUIRED

        def make_connection(self, host):
            # Items in the passed dictionary are passed as keyword
            # arguments to the http.client.HTTPSConnection() constructor.
            # The context argument allows an ssl.SSLContext instance to
            # be passed with information about the SSL configuration
            s = super().make_connection((host, {'context': self._ssl_context}))

            return s

    # Create the client proxy
    s = ServerProxy('https://localhost:15000',
                    transport=VerifyCertSafeTransport('server_cert.pem'),
                    allow_none=True)

服务器将证书发送给客户端，客户端来确认它的合法性。这种确认可以是相互的。
如果服务器想要确认客户端，可以将服务器启动代码修改如下：

.. code-block:: python

    if __name__ == '__main__':
        KEYFILE='server_key.pem'   # Private key of the server
        CERTFILE='server_cert.pem' # Server certificate
        CA_CERTS='client_cert.pem' # Certificates of accepted clients

        kvserv = KeyValueServer(('', 15000),
                                keyfile=KEYFILE,
                                certfile=CERTFILE,
                                ca_certs=CA_CERTS,
                                cert_reqs=ssl.CERT_REQUIRED,
                                )
        kvserv.serve_forever()

为了让XML-RPC客户端发送证书，修改 ``ServerProxy`` 的初始化代码如下：

.. code-block:: python

    # Create the client proxy
    s = ServerProxy('https://localhost:15000',
                    transport=VerifyCertSafeTransport('server_cert.pem',
                                                      'client_cert.pem',
                                                      'client_key.pem'),
                    allow_none=True)

|

----------
讨论
----------
试着去运行本节的代码能测试你的系统配置能力和理解SSL。
可能最大的挑战是如何一步步的获取初始配置key、证书和其他所需依赖。

我解释下到底需要啥，每一个SSL连接终端一般都会有一个私钥和一个签名证书文件。
这个证书包含了公钥并在每一次连接的时候都会发送给对方。
对于公共服务器，它们的证书通常是被权威证书机构比如Verisign、Equifax或其他类似机构（需要付费的）签名过的。
为了确认服务器签名，客户端回保存一份包含了信任授权机构的证书列表文件。
例如，web浏览器保存了主要的认证机构的证书，并使用它来为每一个HTTPS连接确认证书的合法性。
对本小节示例而言，只是为了测试，我们可以创建自签名的证书，下面是主要步骤：


    bash % openssl req -new -x509 -days 365 -nodes -out server_cert.pem \
               -keyout server_key.pem
    Generating a 1024 bit RSA private key
    ..........................................++++++
    ...++++++

    writing new private key to 'server_key.pem'

     -----
    You are about to be asked to enter information that will be incorporated
    into your certificate request.
    What you are about to enter is what is called a Distinguished Name or a DN.
    There are quite a few fields but you can leave some blank
    For some fields there will be a default value,
    If you enter '.', the field will be left blank.
     -----
    Country Name (2 letter code) [AU]:US
    State or Province Name (full name) [Some-State]:Illinois
    Locality Name (eg, city) []:Chicago
    Organization Name (eg, company) [Internet Widgits Pty Ltd]:Dabeaz, LLC
    Organizational Unit Name (eg, section) []:
    Common Name (eg, YOUR name) []:localhost
    Email Address []:
    bash %

在创建证书的时候，各个值的设定可以是任意的，但是”Common Name“的值通常要包含服务器的DNS主机名。
如果你只是在本机测试，那么就使用”localhost“，否则使用服务器的域名。

    -----BEGIN RSA PRIVATE KEY-----
    MIICXQIBAAKBgQCZrCNLoEyAKF+f9UNcFaz5Osa6jf7qkbUl8si5xQrY3ZYC7juu
    nL1dZLn/VbEFIITaUOgvBtPv1qUWTJGwga62VSG1oFE0ODIx3g2Nh4sRf+rySsx2
    L4442nx0z4O5vJQ7k6eRNHAZUUnCL50+YvjyLyt7ryLSjSuKhCcJsbZgPwIDAQAB
    AoGAB5evrr7eyL4160tM5rHTeATlaLY3UBOe5Z8XN8Z6gLiB/ucSX9AysviVD/6F
    3oD6z2aL8jbeJc1vHqjt0dC2dwwm32vVl8mRdyoAsQpWmiqXrkvP4Bsl04VpBeHw
    Qt8xNSW9SFhceL3LEvw9M8i9MV39viih1ILyH8OuHdvJyFECQQDLEjl2d2ppxND9
    PoLqVFAirDfX2JnLTdWbc+M11a9Jdn3hKF8TcxfEnFVs5Gav1MusicY5KB0ylYPb
    YbTvqKc7AkEAwbnRBO2VYEZsJZp2X0IZqP9ovWokkpYx+PE4+c6MySDgaMcigL7v
    WDIHJG1CHudD09GbqENasDzyb2HAIW4CzQJBAKDdkv+xoW6gJx42Auc2WzTcUHCA
    eXR/+BLpPrhKykzbvOQ8YvS5W764SUO1u1LWs3G+wnRMvrRvlMCZKgggBjkCQQCG
    Jewto2+a+WkOKQXrNNScCDE5aPTmZQc5waCYq4UmCZQcOjkUOiN3ST1U5iuxRqfb
    V/yX6fw0qh+fLWtkOs/JAkA+okMSxZwqRtfgOFGBfwQ8/iKrnizeanTQ3L6scFXI
    CHZXdJ3XQ6qUmNxNn7iJ7S/LDawo1QfWkCfD9FYoxBlg
    -----END RSA PRIVATE KEY-----

服务器证书文件server_cert.pem内容类似下面这样：

    -----BEGIN CERTIFICATE-----
    MIIC+DCCAmGgAwIBAgIJAPMd+vi45js3MA0GCSqGSIb3DQEBBQUAMFwxCzAJBgNV
    BAYTAlVTMREwDwYDVQQIEwhJbGxpbm9pczEQMA4GA1UEBxMHQ2hpY2FnbzEUMBIG
    A1UEChMLRGFiZWF6LCBMTEMxEjAQBgNVBAMTCWxvY2FsaG9zdDAeFw0xMzAxMTEx
    ODQyMjdaFw0xNDAxMTExODQyMjdaMFwxCzAJBgNVBAYTAlVTMREwDwYDVQQIEwhJ
    bGxpbm9pczEQMA4GA1UEBxMHQ2hpY2FnbzEUMBIGA1UEChMLRGFiZWF6LCBMTEMx
    EjAQBgNVBAMTCWxvY2FsaG9zdDCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEA
    mawjS6BMgChfn/VDXBWs+TrGuo3+6pG1JfLIucUK2N2WAu47rpy9XWS5/1WxBSCE
    2lDoLwbT79alFkyRsIGutlUhtaBRNDgyMd4NjYeLEX/q8krMdi+OONp8dM+DubyU

    O5OnkTRwGVFJwi+dPmL48i8re68i0o0rioQnCbG2YD8CAwEAAaOBwTCBvjAdBgNV
    HQ4EFgQUrtoLHHgXiDZTr26NMmgKJLJLFtIwgY4GA1UdIwSBhjCBg4AUrtoLHHgX
    iDZTr26NMmgKJLJLFtKhYKReMFwxCzAJBgNVBAYTAlVTMREwDwYDVQQIEwhJbGxp
    bm9pczEQMA4GA1UEBxMHQ2hpY2FnbzEUMBIGA1UEChMLRGFiZWF6LCBMTEMxEjAQ
    BgNVBAMTCWxvY2FsaG9zdIIJAPMd+vi45js3MAwGA1UdEwQFMAMBAf8wDQYJKoZI
    hvcNAQEFBQADgYEAFci+dqvMG4xF8UTnbGVvZJPIzJDRee6Nbt6AHQo9pOdAIMAu
    WsGCplSOaDNdKKzl+b2UT2Zp3AIW4Qd51bouSNnR4M/gnr9ZD1ZctFd3jS+C5XRp
    D3vvcW5lAnCCC80P6rXy7d7hTeFu5EYKtRGXNvVNd/06NALGDflrrOwxF3Y=
    -----END CERTIFICATE-----

在服务器端代码中，私钥和证书文件会被传给SSL相关的包装函数。证书来自于客户端，
私钥应该在保存在服务器中，并加以安全保护。

在客户端代码中，需要保存一个合法证书授权文件来确认服务器证书。
如果你没有这个文件，你可以在客户端复制一份服务器的证书并使用它来确认。
连接建立后，服务器会提供它的证书，然后你就能使用已经保存的证书来确认它是否正确。

服务器也能选择是否要确认客户端的身份。如果要这样做的话，客户端需要有自己的私钥和认证文件。
服务器也需要保存一个被信任证书授权文件来确认客户端证书。

如果你要在真实环境中为你的网络服务加上SSL的支持，这小节只是一个入门介绍而已。
你还应该参考其他的文档，做好花费不少时间来测试它正常工作的准备。反正，就是得慢慢折腾吧~ ^_^

