#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic:
        collections中几个有用的数据结构

    deque: 高效的双端队列
    defaultdict: 类似dict，对于缺少key处理更优雅
    namedtuple: 命名tuple

"""
from collections import deque
from collections import defaultdict
from collections import namedtuple
__author__ = 'Xiong Neng'


def main():
    s = "yeah but no but yeah but no test good"
    words = s.split()
    # key不存在时调用list()函数，并保存为key对应的value
    word_locs = defaultdict(list)
    for n, w in enumerate(words):
        word_locs[w].append(n)
    print(word_locs)

    # 如果定义仅用作数据结构的对象，最好使用命名tuple，无需定义一个类
    network_address = namedtuple('network', ['hostname', 'port'])
    a = network_address('www.python.org', 80)
    print(a.hostname, a.port, sep='-')
    print(type(a))  # <class '__main__.network'>
    pass


if __name__ == '__main__':
    main()
