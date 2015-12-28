===========================
10.7 运行目录或压缩文件
===========================

----------
问题
----------
您有已经一个复杂的脚本到涉及多个文件的应用程序。你想有一些简单的方法让用户运行程序。

----------
解决方案
----------
如果你的应用程序已经有多个文件，你可以把你的应用程序放进它自己的目录并添加一个__main__.py文件。 举个例子，你可以像这样创建目录：

.. code-block:: python

    myapplication/
        spam.py
        bar.py
        grok.py
        __main__.py

如果__main__.py存在，你可以简单地在顶级目录运行Python解释器：

.. code-block:: python

    bash % python3 myapplication

解释器将执行__main__.py文件作为主程序。

如果你将你的代码打包成zip文件，这种技术同样也适用，举个例子：

.. code-block:: python

    bash % ls
    spam.py bar.py grok.py __main__.py
    bash % zip -r myapp.zip *.py
    bash % python3 myapp.zip
    ... output from __main__.py ...

----------
讨论
----------
创建一个目录或zip文件并添加__main__.py文件来将一个更大的Python应用打包是可行的。这和作为标准库被安装到Python库的代码包是有一点区别的。相反，这只是让别人执行的代码包。


由于目录和zip文件与正常文件有一点不同，你可能还需要增加一个shell脚本，使执行更加容易。例如，如果代码文件名为myapp.zip，你可以创建这样一个顶级脚本：


.. code-block:: bash

    #!/usr/bin/env python3 /usr/local/bin/myapp.zip

