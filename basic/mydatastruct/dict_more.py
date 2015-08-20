#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 字典dict数据结构
Desc : 
    
"""


def dict_demo():
    aa = ('2', '3')
    bb = {aa: '3333'}
    tel = {'jack': 4098, 'sape': 4139}
    tel = dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
    # 字典推导式
    tel = {x: x*2 for x in range(1, 6)}
    # 删除
    del tel[2]
    print(tel)


if __name__ == '__main__':
    dict_demo()

