==============================
5.12 测试文件是否存在
==============================

----------
问题
----------
你想测试一个文件或目录是否存在。

|

----------
解决方案
----------
使用 ``os.path`` 模块来测试一个文件或目录是否存在。比如：

.. code-block:: python

    >>> import os
    >>> os.path.exists('/etc/passwd')
    True
    >>> os.path.exists('/tmp/spam')
    False
    >>>

你还能进一步测试这个文件时什么类型的。
在下面这些测试中，如果测试的文件不存在的时候，结果都会返回False：

.. code-block:: python

    >>> # Is a regular file
    >>> os.path.isfile('/etc/passwd')
    True

    >>> # Is a directory
    >>> os.path.isdir('/etc/passwd')
    False

    >>> # Is a symbolic link
    >>> os.path.islink('/usr/local/bin/python3')
    True

    >>> # Get the file linked to
    >>> os.path.realpath('/usr/local/bin/python3')
    '/usr/local/bin/python3.3'
    >>>

如果你还想获取元数据(比如文件大小或者是修改日期)，也可以使用 ``os.path`` 模块来解决：

.. code-block:: python

    >>> os.path.getsize('/etc/passwd')
    3669
    >>> os.path.getmtime('/etc/passwd')
    1272478234.0
    >>> import time
    >>> time.ctime(os.path.getmtime('/etc/passwd'))
    'Wed Apr 28 13:10:34 2010'
    >>>

|

----------
讨论
----------
使用 ``os.path`` 来进行文件测试是很简单的。
在写这些脚本时，可能唯一需要注意的就是你需要考虑文件权限的问题，特别是在获取元数据时候。比如：

.. code-block:: python

    >>> os.path.getsize('/Users/guido/Desktop/foo.txt')
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "/usr/local/lib/python3.3/genericpath.py", line 49, in getsize
            return os.stat(filename).st_size
    PermissionError: [Errno 13] Permission denied: '/Users/guido/Desktop/foo.txt'
    >>>

