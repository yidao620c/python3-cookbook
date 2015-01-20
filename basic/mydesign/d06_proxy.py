#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 代理模式
Desc : 代理模式，也叫委托模式 是一个使用率非常高的模式，
       非常典型的场景就是游戏代练，代练者就是一个代理者或者委托者。
"""


class RealSubject:
    def request(self):
        print('核心业务逻辑')


class Proxy(RealSubject):
    def __init__(self):
        self.real_subject = RealSubject()

    def request(self):
        self.before()
        self.real_subject.request()
        self.end()

    def before(self):
        print('before')

    def end(self):
        print('end')

if __name__ == '__main__':
    p = Proxy()
    p.request()
