==============================
5.11 文件路径名的操作
==============================

----------
问题
----------
你需要使用路径名来获取文件名，目录名，绝对路径等等。

----------
解决方案
----------
使用 ``os.path`` 模块中的函数来操作路径名。
下面是一个交互式例子来演示一些关键的特性：

.. code-block:: python

    >>> import os
    >>> path = '/Users/beazley/Data/data.csv'

    >>> # Get the last component of the path
    >>> os.path.basename(path)
    'data.csv'

    >>> # Get the directory name
    >>> os.path.dirname(path)
    '/Users/beazley/Data'

    >>> # Join path components together
    >>> os.path.join('tmp', 'data', os.path.basename(path))
    'tmp/data/data.csv'

    >>> # Expand the user's home directory
    >>> path = '~/Data/data.csv'
    >>> os.path.expanduser(path)
    '/Users/beazley/Data/data.csv'

    >>> # Split the file extension
    >>> os.path.splitext(path)
    ('~/Data/data', '.csv')
    >>>

----------
讨论
----------
对于任何的文件名的操作，你都应该使用 ``os.path`` 模块，而不是使用标准字符串操作来构造自己的代码。
特别是为了可移植性考虑的时候更应如此，
因为 ``os.path`` 模块知道Unix和Windows系统之间的差异并且能够可靠地处理类似 ``Data/data.csv``
和 ``Data\data.csv`` 这样的文件名。
其次，你真的不应该浪费时间去重复造轮子。通常最好是直接使用已经为你准备好的功能。

要注意的是 ``os.path`` 还有更多的功能在这里并没有列举出来。
可以查阅官方文档来获取更多与文件测试，符号链接等相关的函数说明。

