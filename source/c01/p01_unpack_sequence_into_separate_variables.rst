===============================
解压序列赋值给多个变量
===============================

----------
问题
----------
You have an N-element tuple or sequence that you would like to unpack into a collection of N variables.

----------
解决方案
----------
Any sequence (or iterable) can be unpacked into variables using a simple assignment operation. The only requirement is that the number of variables and structure match the sequence. For example:

----------
讨论
----------
Unpacking actually works with any object that happens to be iterable, not just tuples or lists. This includes strings, files, iterators, and generators. For example: