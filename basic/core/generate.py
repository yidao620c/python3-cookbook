# encoding: utf-8
"""
    Topic: 生成器表达式
    Desc:
    生成器是特定的函数，允许你返回一个值，然后'暂停'代码执行，稍后恢复。
    列表解析的一个不足就是要一次性生成所有数据，对大量数据的迭代器是不好的
    生成器表达式：生成器 + 列表解析，解决了这个问题

    列表解析：
    [expr for var in iterable if cond]
    生成器表达式：
    (expr for var in iterable if cond)
"""
__author__ = 'Xiong Neng'


def my_generate():
    # 继续前面的例子，统计文件中非空字符的个数，sum()参数可以是列表，还可以是可迭代对象
    # 统计文件中非空字符个数
    f = open('readme.txt', 'r')
    f.seek(0)
    print(sum(len(word) for line in f for word in line.split()))
    # 我们只是把括号删除：少了两个字节，而且更省内存 ... 灰常地环保
    rows = [1, 2, 3, 16]

    x_pairs = ((i, j) for i in rows for j in cols())
    print(type(x_pairs))
    print(x_pairs)
    for pair in x_pairs:
        print(type(pair), pair)

    # 获取文件中最长的行的长度
    # print(max(len(x.strip()) for x in open('/etc/motd')))

    a = input('input... ')
    print(type(a))


def cols():
    print("in cols...")
    yield 44
    print("in cols...")
    yield 34
    print("in cols...")
    yield 7


def my_next():
    aa = cols()
    print("start to invoke __next__() method..")
    print(aa.__next__())
    print(aa.__next__())
    print(aa.__next__())


if __name__ == "__main__":
    my_next()