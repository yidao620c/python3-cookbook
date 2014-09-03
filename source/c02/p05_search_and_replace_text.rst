========================
2.5 字符串搜索和替换
========================

----------
问题
----------
你想在字符串中搜索和匹配指定的文本模式

|

----------
解决方案
----------
对于简单的字面模式，直接使用str.repalce()方法即可，比如：

.. code-block:: python

    >>> text = 'yeah, but no, but yeah, but no, but yeah'
    >>> text.replace('yeah', 'yep')
    'yep, but no, but yep, but no, but yep'
    >>>

对于复杂的模式，请使用re模块中的sub()函数。
为了说明这个，假设你想将形式为"11/27/201"的日期字符串改成"2012-11-27"。示例如下：

.. code-block:: python

    >>> text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
    >>> import re
    >>> re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text)
    'Today is 2012-11-27. PyCon starts 2013-3-13.'
    >>>

sub()函数中的第一个参数是被匹配的模式，第二个参数是替换模式。反斜杠数字比如\3指向前面模式的捕获组号。

如果你打算用相同的模式做多次替换，考虑先编译它来提升性能。比如：

.. code-block:: python

    >>> import re
    >>> datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
    >>> datepat.sub(r'\3-\1-\2', text)
    'Today is 2012-11-27. PyCon starts 2013-3-13.'
    >>>

对于更加复杂的替换，可以传递一个替换回调函数来代替，比如：

.. code-block:: python

    >>> from calendar import month_abbr
    >>> def change_date(m):
    ... mon_name = month_abbr[int(m.group(1))]
    ... return '{} {} {}'.format(m.group(2), mon_name, m.group(3))
    ...
    >>> datepat.sub(change_date, text)
    'Today is 27 Nov 2012. PyCon starts 13 Mar 2013.'
    >>>

一个替换回调函数的参数是一个match对象，也就是match()或者find()返回的对象。
使用.group()方法来提取特定的匹配部分。回调函数最后返回替换字符串。

如果除了替换后的结果外，你还想知道有多少替换发生了，可以使用re.subn()来代替。比如：

..  code-block:: python

    >>> newtext, n = datepat.subn(r'\3-\1-\2', text)
    >>> newtext
    'Today is 2012-11-27. PyCon starts 2013-3-13.'
    >>> n
    2
    >>>

|

----------
讨论
----------
There isn’t much more to regular expression search and replace than the sub() method
shown. The trickiest part is specifying the regular expression pattern—something that’s
best left as an exercise to the reader.
