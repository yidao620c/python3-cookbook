==============================
5.21 序列化Python对象
==============================

----------
问题
----------
你需要将一个Python对象序列化为一个字节流，以便将它保存到一个文件、存储到数据库或者通过网络传输它。

|

----------
解决方案
----------
The most common approach for serializing data is to use the pickle module. To dump
an object to a file, you do this:
对于序列化最普遍的做法就是使用 ``pickle`` 模块。为了将一个对象保存到一个文件中，可以这样做：

.. code-block:: python

    import pickle

    data = ... # Some Python object
    f = open('somefile', 'wb')
    pickle.dump(data, f)

为了将一个对象转储为一个字符串，可以使用 ``pickle.dumps()`` ：

.. code-block:: python

    s = pickle.dumps(data)

为了从字节流中恢复一个对象，使用 ``picle.load()`` 或 ``pickle.loads()`` 函数。比如：

.. code-block:: python

    # Restore from a file
    f = open('somefile', 'rb')
    data = pickle.load(f)

    # Restore from a string
    data = pickle.loads(s)

|

----------
讨论
----------
对于大多数应用程序来讲，``dump()`` 和 ``load()`` 函数的使用就是你有效使用 ``pickle`` 模块所需的全部了。
它可适用于绝大部分Python数据类型和用户自定义类的对象实例。
如果你碰到某个库可以让你在数据库中保存/恢复Python对象或者是通过网络传输对象的话，
那么很有可能这个库的底层就使用了 ``pickle`` 模块。

``pickle`` 是一种Python特有的自描述的数据编码。
通过自描述，被序列化后的数据包含每个对象开始和结束以及它的类型的信息。
因此，你无需担心对象记录的定义，它总是能工作。
举个例子，如果要处理多个对象，你可以这样做：

.. code-block:: python

    >>> import pickle
    >>> f = open('somedata', 'wb')
    >>> pickle.dump([1, 2, 3, 4], f)
    >>> pickle.dump('hello', f)
    >>> pickle.dump({'Apple', 'Pear', 'Banana'}, f)
    >>> f.close()
    >>> f = open('somedata', 'rb')
    >>> pickle.load(f)
    [1, 2, 3, 4]
    >>> pickle.load(f)
    'hello'
    >>> pickle.load(f)
    {'Apple', 'Pear', 'Banana'}
    >>>

你还能序列化函数，类，还有接口，但是结果数据仅仅将它们的名称编码成对应的代码对象。例如：

.. code-block:: python

    >>> import math
    >>> import pickle.
    >>> pickle.dumps(math.cos)
    b'\x80\x03cmath\ncos\nq\x00.'
    >>>

当数据反序列化回来的时候，会先假定所有的源数据时可用的。
模块，类和函数会自动按需导入进来。对于Python数据被不同机器上的解析器所共享的应用程序而言，
数据的保存可能会有问题，因为所有的机器都必须访问同一个源代码。


