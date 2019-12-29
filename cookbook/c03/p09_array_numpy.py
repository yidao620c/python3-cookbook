#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 利用numpy执行数组运算
Desc : 
"""
import numpy as np


def array_numpy():
    x = [1, 2, 3, 4]
    y = [5, 6, 7, 8]
    print(x * 2)
    print(x + y)

    # Numpy arrays
    ax = np.array([1, 2, 3, 4])
    ay = np.array([5, 6, 7, 8])
    print(ax * 2)
    print(ax + ay)
    print(ax * ay)

    print(f(ax))
    print(np.sqrt(ax))
    print(np.cos(ax))

    # 大数组
    grid = np.zeros(shape=(10000, 10000), dtype=float)
    grid += 10
    print(grid)
    print(np.sin(grid))

    # 二维数组的索引操作
    a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    print(a)
    print(a[1])  # Select row 1
    print(a[:, 1])  # Select column 1
    # Select a subregion and change it
    print(a[1:3, 1:3])
    a[1:3, 1:3] += 10
    print(a)

    # Broadcast a row vector across an operation on all rows
    print(a + [100, 101, 102, 103])
    # Conditional assignment on an array
    print(np.where(a < 10, a, 10))



def f(x):
    return 3 * x ** 2 - 2 * x + 7


if __name__ == '__main__':
    array_numpy()