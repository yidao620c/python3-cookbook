==========================
2.16 以指定列宽格式化字符串
==========================

----------
问题
----------
你有一些长字符串，想以指定的列宽将它们重新格式化。

|

----------
解决方案
----------
使用 ``textwrap`` 模块来格式化字符串的输出。比如，假如你有下列的长字符串：

.. code-block:: python

    s = "Look into my eyes, look into my eyes, the eyes, the eyes, \
    the eyes, not around the eyes, don't look around the eyes, \
    look into my eyes, you're under."

下面演示使用 ``textwrap`` 格式化字符串的多种方式：

.. code-block:: python

    >>> import textwrap
    >>> print(textwrap.fill(s, 70))
    Look into my eyes, look into my eyes, the eyes, the eyes, the eyes,
    not around the eyes, don't look around the eyes, look into my eyes,
    you're under.

    >>> print(textwrap.fill(s, 40))
    Look into my eyes, look into my eyes,
    the eyes, the eyes, the eyes, not around
    the eyes, don't look around the eyes,
    look into my eyes, you're under.

    >>> print(textwrap.fill(s, 40, initial_indent='    '))
        Look into my eyes, look into my
    eyes, the eyes, the eyes, the eyes, not
    around the eyes, don't look around the
    eyes, look into my eyes, you're under.

    >>> print(textwrap.fill(s, 40, subsequent_indent='    '))
    Look into my eyes, look into my eyes,
        the eyes, the eyes, the eyes, not
        around the eyes, don't look around
        the eyes, look into my eyes, you're
        under.

|

----------
讨论
----------
``textwrap`` 模块对于字符串打印是非常有用的，特别是当你希望输出自动匹配终端大小的时候。
你可以使用 ``os.get_terminal_size()`` 方法来获取终端的大小尺寸。比如：

.. code-block:: python

    >>> import os
    >>> os.get_terminal_size().columns
    80
    >>>

``fill()`` 方法接受一些其他可选参数来控制tab，语句结尾等。
参阅 `textwrap.TextWrapper文档`_ 获取更多内容。

.. _textwrap.TextWrapper文档:
    https://docs.python.org/3.3/library/textwrap.html#textwrap.TextWrapper

