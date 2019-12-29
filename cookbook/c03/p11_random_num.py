#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 随机数
Desc : 
"""
import random


def random_num():
    values = [1, 2, 3, 4, 5, 6]
    print(random.choice(values))
    print(random.choice(values))
    print(random.choice(values))
    print(random.choice(values))
    print(random.choice(values))

    # 抽取样本
    print(random.sample(values, 2))
    print(random.sample(values, 2))
    print(random.sample(values, 3))

    # 打算顺序
    random.shuffle(values)
    print(values)

    # 随机整数
    print(random.randint(0,10))
    print(random.randint(0,10))
    print(random.randint(0,10))
    print(random.randint(0,10))

    # 随机二进制数的整数返回
    print(random.getrandbits(200))

    # 修改随机数生成的种子
    random.seed() # Seed based on system time or os.urandom()
    random.seed(12345) # Seed based on integer given
    random.seed(b'bytedata') # Seed based on byte data

if __name__ == '__main__':
    random_num()

