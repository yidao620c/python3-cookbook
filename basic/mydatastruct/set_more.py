#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 集合set数据结构
Desc : 
    
"""


def set_demo():
    # 初始化一个set
    aset = {1, 2, 2, 3}
    # 一个空的，必须用set()
    aset = set()
    a = set('abracadabra')
    b = set('alacazam')
    # 并 union
    print(a | b)
    # 交 intersection
    print( a & b)
    # 差 difference
    print(a - b)
    # 对称差 symmetric difference
    print(a ^ b)

    # 类似列表推导，其实我们还有集合推导，吊
    print({x for x in 'abracadabra' if x not in 'abc'})

if __name__ == '__main__':
    set_demo()

