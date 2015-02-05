#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: 字符串格式化
    Desc : 
"""

__author__ = 'Xiong Neng'


def simple():
    # 一般的%形式的格式化
    a = 42
    b = 13.142783
    c = 'hello'
    d = {'x': 13, 'y': 1.54321, 'z': 'world'}
    e = 32543263552354234
    print('a is %d' % a)
    print('%10d %f' % (a, b))  # 最小宽度是10，默认空格补全，右对齐
    print('%+010d %E' % (a, b))  # 0补齐， %E科学计数法
    # x左对齐， y最大位数是3(整数和小数位和)
    # 注意，只有%f %e %E是浮点数，%0.3表示小数点后面位数是3，其他数值类型是表示所有数值位个数
    print('%(x)-10d %(y)0.3g' % d)
    print('%0.4s %s' % (c, d['z']))  # 字符串c最大字符个数4,
    print('%*.*f' % (5, 3, b))  # 用后面的参数填充前面格式串
    print('e = %d' % e)
    stock = {
        'name': 'Good',
        'shares': 100,
        'price': 490.10
    }
    print('%(shares)d of %(name)s at %(price)0.2f' % stock)
    # 还可使用var()函数
    name = 'Elwood'
    age = 99
    print('%(name)s is %(age)s years old.' % vars())
    # print('{0} {1} {2}'.format())


def senior():
    """高级字符串格式化"""
    print('{0} {1} {2}'.format('Good', 100, 490.10))
    print('{name} {shares} {price}'.format(name='Good', shares=100, price=490.1))
    print('Hello {0}, your age is {age}'.format('Elwood', age=47))
    print('Use {{ and }} to output single curly braces'.format())
    stock = {
        'name': 'Good',
        'shares': 100,
        'price': 490.10
    }
    print('{name} {shares} {price}'.format(**stock))
    x = 3 + 4.2j
    print('{0.real} {0.imag}'.format(x))
    print('{name:8} {shares:8d} {price:8.2f}'.format(**stock))
    # 格式说明：[fill[align]][sign][0][width][.precision][type]
    # fill填充空白，align可取<或>或^表示左对齐，右对齐，中间对齐
    # width指定最小字段宽度
    # type就是d b o x f e E之类的，但有个%指的是变成百分之多少形式
    name = 'Elwood'
    print('{0:<10}'.format(name))
    print('{0:=^10}'.format(name))  # 中间对齐，并用=填充两边
    y = 3.1415926
    print('{0:{width}.{precision}f}'.format(y, width=10, precision=3))


if __name__ == '__main__':
    simple()
    senior()


