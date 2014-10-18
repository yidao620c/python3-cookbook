============================
6.9 编码和解码十六进制数
============================

----------
问题
----------
你想将一个十六进制字符串解码成一个字节字符串或者将一个字节字符串编码成一个十六进制字符串。

|

----------
解决方案
----------
如果你只是简单的解码或编码一个十六进制的原始字符串，可以使用　``binascii`` 模块。例如：

.. code-block:: python

    >>> # Initial byte string
    >>> s = b'hello'
    >>> # Encode as hex
    >>> import binascii
    >>> h = binascii.b2a_hex(s)
    >>> h
    b'68656c6c6f'
    >>> # Decode back to bytes
    >>> binascii.a2b_hex(h)
    b'hello'
    >>>

类似的功能同样可以在 ``base64`` 模块中找到。例如：

.. code-block:: python

    >>> import base64
    >>> h = base64.b16encode(s)
    >>> h
    b'68656C6C6F'
    >>> base64.b16decode(h)
    b'hello'
    >>>

|

----------
讨论
----------
大部分情况下，通过使用上述的函数来转换十六进制是很简单的。
上面两种技术的主要不同在于大小写的处理。
函数 ``base64.b16decode()`` 和 ``base64.b16encode()`` 只能操作大写形式的十六进制字母，
而 ``binascii`` 模块中的函数大小写都能处理。

还有一点需要注意的是编码函数所产生的输出总是一个字节字符串。
如果想强制以Unicode形式输出，你需要增加一个额外的界面步骤。例如：

.. code-block:: python

    >>> h = base64.b16encode(s)
    >>> print(h)
    b'68656C6C6F'
    >>> print(h.decode('ascii'))
    68656C6C6F
    >>>

在解码十六进制数时，函数 ``b16decode()`` 和 ``a2b_hex()`` 可以接受字节或unicode字符串。
但是，unicode字符串必须仅仅只包含ASCII编码的十六进制数。
