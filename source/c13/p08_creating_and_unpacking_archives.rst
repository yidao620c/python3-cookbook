==============================
13.8 创建和解压归档文件
==============================

----------
问题
----------
你需要创建或解压常见格式的归档文件（比如.tar, .tgz或.zip）

----------
解决方案
----------
``shutil`` 模块拥有两个函数—— ``make_archive()`` 和 ``unpack_archive()`` 可派上用场。
例如：

.. code-block:: python

    >>> import shutil
    >>> shutil.unpack_archive('Python-3.3.0.tgz')

    >>> shutil.make_archive('py33','zip','Python-3.3.0')
    '/Users/beazley/Downloads/py33.zip'
    >>>

``make_archive()`` 的第二个参数是期望的输出格式。
可以使用 ``get_archive_formats()`` 获取所有支持的归档格式列表。例如：

.. code-block:: python

    >>> shutil.get_archive_formats()
    [('bztar', "bzip2'ed tar-file"), ('gztar', "gzip'ed tar-file"),
     ('tar', 'uncompressed tar file'), ('zip', 'ZIP file')]
    >>>

----------
讨论
----------
Python还有其他的模块可用来处理多种归档格式（比如tarfile, zipfile, gzip, bz2）的底层细节。
不过，如果你仅仅只是要创建或提取某个归档，就没有必要使用底层库了。
可以直接使用 ``shutil`` 中的这些高层函数。

这些函数还有很多其他选项，用于日志打印、预检、文件权限等等。
参考 `shutil文档 <https://docs.python.org/3/library/shutil.html>`_