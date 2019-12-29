============================
6.10 编码解码Base64数据
============================

----------
问题
----------
你需要使用Base64格式解码或编码二进制数据。

----------
解决方案
----------
``base64`` 模块中有两个函数 ``b64encode()`` and ``b64decode()`` 可以帮你解决这个问题。例如;

.. code-block:: python

    >>> # Some byte data
    >>> s = b'hello'
    >>> import base64

    >>> # Encode as Base64
    >>> a = base64.b64encode(s)
    >>> a
    b'aGVsbG8='

    >>> # Decode from Base64
    >>> base64.b64decode(a)
    b'hello'
    >>>

----------
讨论
----------
Base64编码仅仅用于面向字节的数据比如字节字符串和字节数组。
此外，编码处理的输出结果总是一个字节字符串。
如果你想混合使用Base64编码的数据和Unicode文本，你必须添加一个额外的解码步骤。例如：

.. code-block:: python

    >>> a = base64.b64encode(s).decode('ascii')
    >>> a
    'aGVsbG8='
    >>>

当解码Base64的时候，字节字符串和Unicode文本都可以作为参数。
但是，Unicode字符串只能包含ASCII字符。
