#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 矩阵和线性代数
Desc : 
"""
import numpy as np
import numpy.linalg


def matrix_linear():
    m = np.matrix([[1,-2,3],[0,4,5],[7,8,-9]])
    print(m)

    # Return transpose  转置矩阵
    print(m.T)

    # Return inverse  # 逆矩阵
    print(m.I)


    # Create a vector and multiply
    v = np.matrix([[2],[3],[4]])
    print(v)
    print(m * v)

    # Determinant 行列式
    print(numpy.linalg.det(m))

    # Eigenvalues 特征值
    print(numpy.linalg.eigvals(m))

    # Solve for x in m*x = v
    x = numpy.linalg.solve(m, v)
    print(x)
    print(m * x)
    print(v)



if __name__ == '__main__':
    matrix_linear()
