#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 可管理的属性
Desc : 
"""
import math


class Person:
    def __init__(self, first_name):
        self.first_name = first_name

    # Getter function
    @property
    def first_name(self):
        return self._first_name

    # Setter function
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # Deleter function (optional)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")


a = Person('Guido')
print(a.first_name)  # Calls the getter
# a.first_name = 42  # Calls the setter
# del a.first_name  # Calls the deleter


class Person1:
    def __init__(self, first_name):
        self.set_first_name(first_name)

    # Getter function
    def get_first_name(self):
        return self._first_name

    # Setter function
    def set_first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # Deleter function (optional)
    def del_first_name(self):
        raise AttributeError("Can't delete attribute")

    # Make a property from existing get/set methods
    name = property(get_first_name, set_first_name, del_first_name)


print(Person1.name.fget)
print(Person1.name.fset)
print(Person1.name.fdel)


class Circle:
    """动态计算的property"""

    def __init__(self, radius):
        self.radius = radius

    @property
    def diameter(self):
        return self.radius ** 2

    @property
    def perimeter(self):
        return 2 * math.pi * self.radius

    @property
    def area(self):
        return math.pi * self.radius ** 2


c = Circle(4.0)
print(c.radius)
print(c.area)  # Notice lack of ()