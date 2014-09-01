#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: random随机数模块
    Desc : random中的函数都不是线程安全的，必须使用锁机制
    都是伪随机数，生成的数是确定的，不应用于密码
"""
import random
__author__ = 'Xiong Neng'


def main():
    random.seed()
    # 随机整数
    print(random.getrandbits(3))
    print(random.randint(200, 800))
    print(2, 400, 2)
    # 随机序列
    seq = range(1, 10)
    print(random.choice(seq))
    print(random.sample(seq, 4))
    a = list(seq)
    random.shuffle(a)
    print(a)

    # 实数
    print(random.random())  # [0.0, 1.0)之间的随机实数
    print(random.uniform(2.1, 4.99))  # 一致分布的某个随机数

    pass


if __name__ == '__main__':
    main()
