#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: class和instance的练习
Desc : 
"""
from types import MethodType


class Dog:
    # 可变对象最好不要定义为类变量，防止共享时修改混乱
    kind = 'canine'  # class variable shared by all instances

    def __init__(self, name):
        self.name = name  # instance variable unique to each instance


def change_dog():
    Dog.kind = 'another'


def set_age(self, age):
    print('set age...')
    self.age = age

if __name__ == '__main__':
    a = Dog('adog')
    b = Dog('bdog')
    print(Dog.kind, a.kind, a.name)
    print(Dog.kind, b.kind, b.name)
    change_dog()
    print(Dog.kind, a.kind, a.name)
    print(Dog.kind, b.kind, b.name)

    Dog.set_age = MethodType(set_age, Dog)
    # b = Dog('bdog')
    b.set_age(111)




