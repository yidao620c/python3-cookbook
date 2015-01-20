#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 各种迭代示例
Desc : 
    
"""


def loop_demo():
    # dict的迭代
    knights = {'gallahad': 'the pure', 'robin': 'the brave'}
    for k, v in knights.items():
        print(k, v)

    # sequence序列迭代：
    for i, v in enumerate(['tic', 'tac', 'toe']):
        print(i, v)

    # 同时迭代多个序列，使用zip函数
    questions = ['name', 'quest', 'favorite color']
    answers = ['lancelot', 'the holy grail', 'blue']
    for q, a in zip(questions, answers):
        print('What is your {0}?  It is {1}.'.format(q, a))

    # 反向迭代
    for i in reversed(['name', 'quest', 'favorite color']):
        print(i)

    # 迭代同时修改，使用a[:]隐藏copy一个新对象
    words = ['cat', 'window', 'defenestrate']
    for w in words[:]:
        if len(w) > 6:
            words.insert(0, w)


if __name__ == '__main__':
    loop_demo()
