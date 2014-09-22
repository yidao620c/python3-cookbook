==============================
5.8 固定大小记录的文件迭代
==============================

----------
问题
----------
你想在一个固定长度记录或者数据块的集合上迭代，而不是在一个文件中一行一行的迭代。

|

----------
解决方案
----------
通过下面这个小技巧使用 ``iter`` 和 ``functools.partial()`` 函数：

.. code-block:: python

    from functools import partial

    RECORD_SIZE = 32

    with open('somefile.data', 'rb') as f:
        records = iter(partial(f.read, RECORD_SIZE), b'')
        for r in records:
            ...

这个例子中的 ``records`` 对象是一个可迭代对象，它会不断的产生固定大小的数据块，直到文件末尾。
要注意的是如果总记录大小不是块大小的整数倍的话，最后一个返回元素的字节数会比期望值少。

|

----------
讨论
----------
A little-known feature of the iter() function is that it can create an iterator if you pass
it a callable and a sentinel value. The resulting iterator simply calls the supplied callable
over and over again until it returns the sentinel, at which point iteration stops.

In the solution, the functools.partial is used to create a callable that reads a fixed
number of bytes from a file each time it’s called. The sentinel of b'' is what gets returned
when a file is read but the end of file has been reached.

Last, but not least, the solution shows the file being opened in binary mode. For reading
fixed-sized records, this would probably be the most common case. For text files, reading
line by line (the default iteration behavior) is more common.

