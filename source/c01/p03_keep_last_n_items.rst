================================
1.3 保留最后N个元素
================================

----------
问题
----------
在迭代操作或者其他操作的时候，怎样只保留最后有限几个元素的历史记录？

----------
解决方案
----------
保留有限历史记录正是collections.deque大显身手的时候。比如，下面的代码在多行上面做简单的文本匹配，
并只返回在前N行中匹配成功的行：

.. code-block:: python

    from collections import deque


    def search(lines, pattern, history=5):
        previous_lines = deque(maxlen=history)
        for li in lines:
            if pattern in li:
                yield li, previous_lines
            previous_lines.append(line)

    # Example use on a file
    if __name__ == '__main__':
        with open(r'../../cookbook/somefile.txt') as f:
            for line, prevlines in search(f, 'Python', 5):
                for pline in prevlines:
                    print(pline, end='')
                print(line, end='')
                print('-' * 20)

----------
讨论
----------
我们在写查询元素的代码的时候，通常会使用包含yield表达式的生成器函数，也就是我们上面示例代码中的那样。
这样可以将搜索过程代码和使用搜索结果代码解耦。如果你还不清楚什么是生成器，请参看4.3节。

使用deque(maxlen=N)构造函数会新建一个固定大小的队列。当新的元素加入并且这个队列已满的时候，
最老的元素会自动被移除掉。

代码示例：

.. code-block:: python

    >>> q = deque(maxlen=3)
    >>> q.append(1)
    >>> q.append(2)
    >>> q.append(3)
    >>> q
    deque([1, 2, 3], maxlen=3)
    >>> q.append(4)
    >>> q
    deque([2, 3, 4], maxlen=3)
    >>> q.append(5)
    >>> q
    deque([3, 4, 5], maxlen=3)

尽管你也可以手动在一个列表上实现这一的操作(比如增加、删除等等)。
但是这里的队列方案会更加优雅并且运行得更快些。

更一般的，deque类可以被用在任何你只需要一个简单队列数据结构的场合。
如果你不设置最大队列大小，那么就会得到一个无限大小队列，你可以在队列的两端执行添加和弹出元素的操作。

代码示例：

.. code-block:: python

    >>> q = deque()
    >>> q.append(1)
    >>> q.append(2)
    >>> q.append(3)
    >>> q
    deque([1, 2, 3])
    >>> q.appendleft(4)
    >>> q
    deque([4, 1, 2, 3])
    >>> q.pop()
    3
    >>> q
    deque([4, 1, 2])
    >>> q.popleft()
    4

在队列两端插入或删除元素时间复杂度都是O(1)，而在list的开头插入或删除元素的时间复杂度为O(N)。

