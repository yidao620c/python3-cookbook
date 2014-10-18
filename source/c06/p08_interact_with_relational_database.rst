============================
6.8 与关系型数据库的交互
============================

----------
问题
----------
你想在关系型数据库中查询、增加或删除记录。

|

----------
解决方案
----------
Python中表示多行数据的标准方式是一个由元组构成的序列。例如：

.. code-block:: python

    stocks = [
        ('GOOG', 100, 490.1),
        ('AAPL', 50, 545.75),
        ('FB', 150, 7.45),
        ('HPQ', 75, 33.2),
    ]

依据PEP249，通过这种形式提供数据，
可以很容易的使用Python标准数据库API和关系型数据库进行交互。
所有数据库上的操作都通过SQL查询语句来完成。每一行输入输出数据用一个元组来表示。

为了演示说明，你可以使用Python标准库中的 ``sqlite3`` 模块。
如果你使用的是一个不同的数据库(比如MySql、Postgresql或者ODBC)，
还得安装相应的第三方模块来提供支持。
不过相应的编程接口几乎都是一样的，除了一点点细微差别外。

The first step is to connect to the database. Typically, you execute a connect() function,
supplying parameters such as the name of the database, hostname, username, password,
and other details as needed. For example:
第一步是连接到数据库。通常你要执行 ``connect()`` 函数，
给它提供一些数据库名、主机、用户名、密码和其他必要的一些参数。例如：

.. code-block:: python

    >>> import sqlite3
    >>> db = sqlite3.connect('database.db')
    >>>

为了处理数据，下一步你需要创建一个游标。
一旦你有了游标，那么你就可以执行SQL查询语句了。比如：

.. code-block:: python

    >>> c = db.cursor()
    >>> c.execute('create table portfolio (symbol text, shares integer, price real)')
    <sqlite3.Cursor object at 0x10067a730>
    >>> db.commit()
    >>>

为了向数据库表中插入多条记录，使用类似下面这样的语句：

.. code-block:: python

    >>> c.executemany('insert into portfolio values (?,?,?)', stocks)
    <sqlite3.Cursor object at 0x10067a730>
    >>> db.commit()
    >>>

To perform a query, use a statement such as this:
为了执行某个查询，使用像下面这样的语句：

.. code-block:: python

    >>> for row in db.execute('select * from portfolio'):
    ...     print(row)
    ...
    ('GOOG', 100, 490.1)
    ('AAPL', 50, 545.75)
    ('FB', 150, 7.45)
    ('HPQ', 75, 33.2)
    >>>

如果你想接受用户输入作为参数来执行查询操作，必须确保你使用下面这样的占位符?来进行参数转义：

.. code-block:: python

    >>> min_price = 100
    >>> for row in db.execute('select * from portfolio where price >= ?',
                              (min_price,)):
    ...     print(row)
    ...
    ('GOOG', 100, 490.1)
    ('AAPL', 50, 545.75)
    >>>

----------
讨论
----------
At a low level, interacting with a database is an extremely straightforward thing to do.
You simply form SQL statements and feed them to the underlying module to either
update the database or retrieve data. That said, there are still some tricky details you’ll
need to sort out on a case-by-case basis.


One complication is the mapping of data from the database into Python types. For
entries such as dates, it is most common to use datetime instances from the date
time module, or possibly system timestamps, as used in the time module. For numerical
data, especially financial data involving decimals, numbers may be represented as Dec
imal instances from the decimal module. Unfortunately, the exact mapping varies by
database backend so you’ll have to read the associated documentation.


Another extremely critical complication concerns the formation of SQL statement
strings. You should never use Python string formatting operators (e.g., %) or the .for
mat() method to create such strings. If the values provided to such formatting operators
are derived from user input, this opens up your program to an SQL-injection attack (see
http://xkcd.com/327). The special ? wildcard in queries instructs the database backend
to use its own string substitution mechanism, which (hopefully) will do it safely.


Sadly, there is some inconsistency across database backends with respect to the wildcard.
Many modules use ? or %s, while others may use a different symbol, such as :0 or :1,
to refer to parameters. Again, you’ll have to consult the documentation for the database
module you’re using. The paramstyle attribute of a database module also contains information
about the quoting style.


For simply pulling data in and out of a database table, using the database API is usually
simple enough. If you’re doing something more complicated, it may make sense to use
a higher-level interface, such as that provided by an object-relational mapper. Libraries
such as SQLAlchemy allow database tables to be described as Python classes and for
database operations to be carried out while hiding most of the underlying SQL.