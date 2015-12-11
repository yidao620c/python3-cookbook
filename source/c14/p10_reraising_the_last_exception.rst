==============================
14.10 重新抛出被捕获的异常
==============================

----------
问题
----------
你在一个 ``except`` 块中捕获了一个异常，现在想重新抛出它。

|

----------
解决方案
----------
简单的使用一个单独的 ``rasie`` 语句即可，例如：

::

    >>> def example():
    ...     try:
    ...             int('N/A')
    ...     except ValueError:
    ...             print("Didn't work")
    ...             raise
    ...

    >>> example()
    Didn't work
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 3, in example
    ValueError: invalid literal for int() with base 10: 'N/A'
    >>>

|

----------
讨论
----------
这个问题通常是当你需要在捕获异常后执行某个操作（比如记录日志、清理等），但是之后想将异常传播下去。
一个很常见的用法是在捕获所有异常的处理器中：

.. code-block:: python

    try:
       ...
    except Exception as e:
       # Process exception information in some way
       ...

       # Propagate the exception
       raise

