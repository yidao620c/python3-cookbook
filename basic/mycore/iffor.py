# encoding: utf-8
"""
    Description:
    iterable:
        它必须提供方法obj.__iter__()，该方法返回一个迭代器对象iter
        或者一个定义了__getitem__(index)的对象，当index不合法时引发IndexError。
    iterator:
        iter必须实现一个方法iter.__next__()
        该方法返回下一个对象或者在迭代结束后引发StopIteration异常
"""
__author__ = 'Xiong Neng'


def fibonacci(n):
    """
    产生斐波那契数列的函数
    通过传递参数n，生产一个长度为n的fibonacci数列并返回
    """
    pass


def for_demo():
    """
    for循环的的演示
    """
    words = ["aa", "bb", "cc"]
    # 如果在迭代中想修改集合，请使用集合的备份或者word[:]
    for w in words[:]:
        if w == 'aa':
            words.insert(0, "dd")
            print(len(words))
    print(words)
    # 迭代同时生产index：
    for i, v in enumerate(words):
        print(i, v)
    print("ddd", "dafdf", "ccc")


if __name__ == '__main__':
    print(fibonacci.__doc__)