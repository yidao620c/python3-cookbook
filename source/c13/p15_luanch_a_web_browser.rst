==============================
13.15 启动一个WEB浏览器
==============================

----------
问题
----------
You want to launch a browser from a script and have it point to some URL that you
specify.

|

----------
解决方案
----------
The webbrowser module can be used to launch a browser in a platform-independent
manner. For example:

>>> import webbrowser
>>> webbrowser.open('http://www.python.org')
True
>>>

This opens the requested page using the default browser. If you want a bit more control
over how the page gets opened, you can use one of the following functions:

>>> # Open the page in a new browser window
>>> webbrowser.open_new('http://www.python.org')
True
>>>

>>> # Open the page in a new browser tab
>>> webbrowser.open_new_tab('http://www.python.org')
True
>>>

These will try to open the page in a new browser window or tab, if possible and supported
by the browser.
If you want to open a page in a specific browser, you can use the webbrowser.get()
function to specify a particular browser. For example:

>>> c = webbrowser.get('firefox')
>>> c.open('http://www.python.org')
True
>>> c.open_new_tab('http://docs.python.org')
True
>>>

A full list of supported browser names can be found in the Python documentation.

|

----------
讨论
----------
Being able to easily launch a browser can be a useful operation in many scripts. For
example, maybe a script performs some kind of deployment to a server and you’d like
to have it quickly launch a browser so you can verify that it’s working. Or maybe a
program writes data out in the form of HTML pages and you’d just like to fire up a
browser to see the result. Either way, the webbrowser module is a simple solution.

