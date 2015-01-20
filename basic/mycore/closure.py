# encoding: utf-8
"""
    Topic: sample
    Desc :
        闭包
"""
__author__ = 'Xiong Neng'


def counter(start_at=0):
    count = [start_at]  # 使用数组是因为在内部函数内，再对这个变量赋值会报错

    def incr():
        # count = count + 1  # 这个就是不合法的
        count[0] += 1  # 单独count赋值操作是不允许的，但是count[0]赋值是可以的。
        return count[0]

    return incr


def countdown(n):
    def cnext():
        nonlocal n  # 使用nonlocal可以将变量声明为外部变量了
        r = n
        n -= 1
        return r

    return cnext


def magic_closure():
    # python中的闭包是后期绑定，运行时绑定
    flist = []
    for i in range(3):
        flist.append(lambda: i)
    print([f() for f in flist])  # [2, 2, 2], strange, ha?
    flist = []
    for i in range(3):
        flist.append(lambda x=i: x)  # 使用默认参数
    print([f() for f in flist])  # [0, 1, 2]  cool


def main():
    ne = countdown(10)
    while True:
        v = ne()
        print(v)
        if not v: break

    magic_closure()
    aa = 3
    if aa <= aa:
        pass

if __name__ == '__main__':
    main()