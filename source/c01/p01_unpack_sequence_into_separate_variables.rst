===============================
1.1 解压序列赋值给多个变量
===============================

----------
问题
----------
现在有一个包含N个元素的元组或者是序列，怎样将它里面的值解压后同时赋值给N变量？

|

----------
解决方案
----------
任何的序列(或者是可迭代对象)可以通过一个简单的赋值语句解压并赋值给多个变量。
唯一的前提就是变量的数量必须跟序列元素的数量是一样的。

代码示例：

.. code-block:: python

    >>> p = (4, 5)
    >>> x, y = p
    >>> x
    4
    >>> y
    5
    >>>
    >>> data = [ 'ACME', 50, 91.1, (2012, 12, 21) ]
    >>> name, shares, price, date = data
    >>> name
    'ACME'
    >>> date
    (2012, 12, 21)
    >>> name, shares, price, (year, mon, day) = data
    >>> name
    'ACME'
    >>> year
    2012
    >>> mon
    12
    >>> day
    21
    >>>

如果变量个数和序列元素的个数不匹配，会产生一个异常。

代码示例：

.. code-block:: python

    >>> p = (4, 5)
    >>> x, y, z = p
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    ValueError: need more than 2 values to unpack
    >>>

|

----------
讨论
----------
实际上，这种解压赋值可以用在任何可迭代对象上面，而不仅仅是列表或者元组。
包括字符串，文件对象，迭代器和生成器。

代码示例：

.. code-block:: python

    >>> s = 'Hello'
    >>> a, b, c, d, e = s
    >>> a
    'H'
    >>> b
    'e'
    >>> e
    'o'
    >>>

有时候，你可能只想解压一部分，丢弃其他的值。对于这种情况Python并没有提供特殊的语法。
但是你可以使用任意变量名去占位，到时候丢掉这些变量就行了。

代码示例：

.. code-block:: python

    >>> data = [ 'ACME', 50, 91.1, (2012, 12, 21) ]
    >>> _, shares, price, _ = data
    >>> shares
    50
    >>> price
    91.1
    >>>

你必须保证你选用的那些占位变量名在其他地方没被使用到。