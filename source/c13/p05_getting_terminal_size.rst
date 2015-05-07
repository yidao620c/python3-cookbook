==============================
13.5 获取终端的大小
==============================

----------
问题
----------
You need to get the terminal size in order to properly format the output of your program.

Solution
Use the os.get_terminal_size() function to do this:

>>> import os
>>> sz = os.get_terminal_size()
>>> sz
os.terminal_size(columns=80, lines=24)
>>> sz.columns
80
>>> sz.lines
24
>>>

Discussion
There are many other possible approaches for obtaining the terminal size, ranging from
reading environment variables to executing low-level system calls involving ioctl()
and TTYs. Frankly, why would you bother with that when this one simple call will
suffice?
