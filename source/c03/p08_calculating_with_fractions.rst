============================
3.8 分数运算
============================

----------
问题
----------
你进入时间机器，突然发现你正在做小学家庭作业，并涉及到分数计算问题。
或者你可能需要写代码去计算在你的木工工厂中的测量值。

----------
解决方案
----------
``fractions`` 模块可以被用来执行包含分数的数学运算。比如：

.. code-block:: python

    >>> from fractions import Fraction
    >>> a = Fraction(5, 4)
    >>> b = Fraction(7, 16)
    >>> print(a + b)
    27/16
    >>> print(a * b)
    35/64

    >>> # Getting numerator/denominator
    >>> c = a * b
    >>> c.numerator
    35
    >>> c.denominator
    64

    >>> # Converting to a float
    >>> float(c)
    0.546875

    >>> # Limiting the denominator of a value
    >>> print(c.limit_denominator(8))
    4/7

    >>> # Converting a float to a fraction
    >>> x = 3.75
    >>> y = Fraction(*x.as_integer_ratio())
    >>> y
    Fraction(15, 4)
    >>>

----------
讨论
----------
在大多数程序中一般不会出现分数的计算问题，但是有时候还是需要用到的。
比如，在一个允许接受分数形式的测试单位并以分数形式执行运算的程序中，
直接使用分数可以减少手动转换为小数或浮点数的工作。

