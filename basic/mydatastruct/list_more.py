#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: list数据结构
Desc : 
    
"""


def list_methods():
    alist = [1, 2, 3, 4]
    # 结论就是讲某个数组插入数组alist的位置i上，执行alist[i:i]=[...]
    alist[4:4] = [9, 10, 11, 12]
    # 删除某个或者某字段的list，请使用del
    del alist[1:3]
    # 情况list
    del alist[:]
    print(alist)


def transpose_list():
    """矩阵转置"""
    matrix = [[1, 2, 3, 4],[5, 6, 7, 8],[9, 10, 11, 12],]
    result = zip(*matrix)
    print(type(result))
    for z in result: print(z)
    # zip是一个可迭代对象，迭代完了就到尾了，后面木有元素了
    result = list(result)
    print(result)

if __name__ == '__main__':
    transpose_list()

