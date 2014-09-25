==============================
5.17 将字节写入文本文件
==============================

----------
问题
----------
你想向以文本模式打开的文件中写入原始的字节数据。

|

----------
解决方案
----------
将字节数据直接写入带缓冲的文件即可，例如：

.. code-block:: python

    >>> import sys
    >>> sys.stdout.write(b'Hello\n')
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
    TypeError: must be str, not bytes
    >>> sys.stdout.buffer.write(b'Hello\n')
    Hello
    5
    >>>


----------
讨论
----------
todo...