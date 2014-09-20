============================
5.1 读写文本数据
============================

----------
问题
----------
你需要读写各种不同编码的文本数据，比如ASCII，UTF-8或者UTF-16编码等。

|

----------
解决方案
----------
使用带有rt模式的open()函数读取文本文件。如下所示：

.. code-block:: python

    # Read the entire file as a single string
    with open('somefile.txt', 'rt') as f:
        data = f.read()

    # Iterate over the lines of the file
    with open('somefile.txt', 'rt') as f:
        for line in f:
            # process line
            ...

类似的，为了写入一个文本文件，使用带有wt模式的open()函数，如果之前文件内容存在则清除并覆盖掉。如下所示：

.. code-block:: python

    # Write chunks of text data
    with open('somefile.txt', 'wt') as f:
        f.write(text1)
        f.write(text2)
        ...

    # Redirected print statement
    with open('somefile.txt', 'wt') as f:
        print(line1, file=f)
        print(line2, file=f)
        ...

如果是在已存在文件中添加内容，使用模式为at的open()函数。

文件的读写操作默认使用系统编码，可以通过调用sys.getdefaultencoding()来得到。
在大多数机器上面都是utf-8编码。如果你已经知道你要读写的文本是其他编码方式，
那么可以通过传递一个科学的encoding参数给open()函数。如下所示：

.. code-block:: python

    with open('somefile.txt', 'rt', encoding='latin-1') as f:
        ...

Python支持非常多的文本编码。几个常见的编码是ascii, latin-1, utf-8和utf-16。
在web应用程序中通常都使用的是UTF-8。
ascii对应从U+0000到U+007F范围内的7位字符。
latin-1是字节0-255到U+0000至U+00FF范围内Unicode字符的直接映射。
当读取一个未知编码的文本时使用latin-1编码永远不会产生解码错误。
使用latin-1编码读取一个文件的时候也许不能产生完全正确的文本解码数据，
但是它也能从中提取出足够多的有用数据。同时，如果你之后将数据回写回去，原先的数据还是会保留的。

|

----------
讨论
----------
Reading and writing text files is typically very straightforward. However, there are a
number of subtle aspects to keep in mind. First, the use of the with statement in the
examples establishes a context in which the file will be used. When control leaves the
with block, the file will be closed automatically. You don’t need to use the with statement,
but if you don’t use it, make sure you remember to close the file:
