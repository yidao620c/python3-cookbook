==============================
13.15 启动一个WEB浏览器
==============================

----------
问题
----------
你想通过脚本启动浏览器并打开指定的URL网页

|

----------
解决方案
----------
``webbrowser`` 模块能被用来启动一个浏览器，并且与平台无关。例如：

.. code-block:: python

    >>> import webbrowser
    >>> webbrowser.open('http://www.python.org')
    True
    >>>

它会使用默认浏览器打开指定网页。如果你还想对网页打开方式做更多控制，还可以使用下面这些函数：

.. code-block:: python

    >>> # Open the page in a new browser window
    >>> webbrowser.open_new('http://www.python.org')
    True
    >>>

    >>> # Open the page in a new browser tab
    >>> webbrowser.open_new_tab('http://www.python.org')
    True
    >>>

这样就可以打开一个新的浏览器窗口或者标签，只要浏览器支持就行。

如果你想指定浏览器类型，可以使用 ``webbrowser.get()`` 函数来指定某个特定浏览器。例如：

.. code-block:: python

    >>> c = webbrowser.get('firefox')
    >>> c.open('http://www.python.org')
    True
    >>> c.open_new_tab('http://docs.python.org')
    True
    >>>

对于支持的浏览器名称列表可查阅`Python文档 <http://docs.python.org/3/library/webbrowser.html>`_

|

----------
讨论
----------
在脚本中打开浏览器有时候会很有用。例如，某个脚本执行某个服务器发布任务，
你想快速打开一个浏览器来确保它已经正常运行了。
或者是某个程序以HTML网页格式输出数据，你想打开浏览器查看结果。
不管是上面哪种情况，使用 ``webbrowser`` 模块都是一个简单实用的解决方案。

