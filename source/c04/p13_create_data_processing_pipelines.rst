============================
4.13 创建数据处理管道
============================

----------
问题
----------
你想以数据管道(类似Unix管道)的方式迭代处理数据。
比如，你有个大量的数据需要处理，但是不能将它们一次性放入内存中。

|

----------
解决方案
----------
生成器函数是一个实现管道机制的好办法。
为了演示，假定你要处理一个非常大的日志文件目录：

.. code-block:: python

    foo/
        access-log-012007.gz
        access-log-022007.gz
        access-log-032007.gz
        ...
        access-log-012008
    bar/
        access-log-092007.bz2
        ...
        access-log-022008

假设每个日志文件包含这样的数据：

.. code-block:: python

    124.115.6.12 - - [10/Jul/2012:00:18:50 -0500] "GET /robots.txt ..." 200 71
    210.212.209.67 - - [10/Jul/2012:00:18:51 -0500] "GET /ply/ ..." 200 11875
    210.212.209.67 - - [10/Jul/2012:00:18:51 -0500] "GET /favicon.ico ..." 404 369
    61.135.216.105 - - [10/Jul/2012:00:20:04 -0500] "GET /blog/atom.xml ..." 304 -
    ...

为了处理这些文件，你可以定义一个由多个执行特定任务独立任务的简单生成器函数组成的容器。就像这样：

.. code-block:: python

    import os
    import fnmatch
    import gzip
    import bz2
    import re

    def gen_find(filepat, top):
        '''
        Find all filenames in a directory tree that match a shell wildcard pattern
        '''
        for path, dirlist, filelist in os.walk(top):
            for name in fnmatch.filter(filelist, filepat):
                yield os.path.join(path,name)

    def gen_opener(filenames):
        '''
        Open a sequence of filenames one at a time producing a file object.
        The file is closed immediately when proceeding to the next iteration.
        '''
        for filename in filenames:
            if filename.endswith('.gz'):
                f = gzip.open(filename, 'rt')
            elif filename.endswith('.bz2'):
                f = bz2.open(filename, 'rt')
            else:
                f = open(filename, 'rt')
            yield f
            f.close()

    def gen_concatenate(iterators):
        '''
        Chain a sequence of iterators together into a single sequence.
        '''
        for it in iterators:
            yield from it

    def gen_grep(pattern, lines):
        '''
        Look for a regex pattern in a sequence of lines
        '''
        pat = re.compile(pattern)
        for line in lines:
            if pat.search(line):
                yield line

现在你可以很容易的将这些函数连起来创建一个处理管道。
比如，为了查找包含单词python的所有日子行，你可以这样做：

.. code-block:: python

    lognames = gen_find('access-log*', 'www')
    files = gen_opener(lognames)
    lines = gen_concatenate(files)
    pylines = gen_grep('(?i)python', lines)
    for line in pylines:
        print(line)

如果将来的时候你想扩展管道，你甚至可以在生成器表达式中包装数据。
比如，下面这个版本计算出传输的字节数并计算其总和。

.. code-block:: python

    lognames = gen_find('access-log*', 'www')
    files = gen_opener(lognames)
    lines = gen_concatenate(files)
    pylines = gen_grep('(?i)python', lines)
    bytecolumn = (line.rsplit(None,1)[1] for line in pylines)
    bytes = (int(x) for x in bytecolumn if x != '-')
    print('Total', sum(bytes))

|

----------
讨论
----------
以管道方式处理数据可以用来解决各类其他问题，包括解析，读取实时数据，定时轮询等。

In understanding the code, it is important to grasp that the yield statement acts as a
kind of data producer whereas a for loop acts as a data consumer. When the generators
are stacked together, each yield feeds a single item of data to the next stage of the
pipeline that is consuming it with iteration. In the last example, the sum() function is
actually driving the entire program, pulling one item at a time out of the pipeline of
generators.
为了理解上述代码，重点是要明白yield语句作为数据的生产者而for循环语句作为数据的消费者。
当这些生成器被连在一起后，每个yield会将一个单独的数据元素传递给迭代处理管道的下一阶段。
在例子最后部分

