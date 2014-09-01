# encoding: utf-8
"""
    Topic: 演示简单的命令行加减运算
    Desc : 
"""
from operator import add, sub
from random import randint, choice

__author__ = 'Xiong Neng'

# 参数列表调用语法：
# position_args: 位置参数
# keword_args: 关键字参数
# tuple_grp_nonkw_args: 元组形式的位置参数
# dict_grp_kw_args: 装有关键字参数的字典
# func(position_args, keword_args, *tuple_grp_nonkw_args, **dict_grp_kw_args)

ops = {'+': add, '-': sub}
MAXTRIES = 2


def doprob():
    op = choice('+-')
    nums = [randint(1, 10) for i in range(2)]
    nums.sort(reverse=True)
    ans = ops[op](*nums)
    pr = '%d %s %d = ' % (nums[0], op, nums[1])
    oops = 0
    while True:
        try:
            if int(input(pr)) == ans:
                print('correct')
                break
            if oops == MAXTRIES:
                print('answer\n%s%d' % (pr, ans))
            else:
                print('incorrect... try again')
                oops += 1
        except (KeyboardInterrupt, EOFError, ValueError) as e:
            print('invalid input... try again.', str(e))
            break


def main():
    while True:
        doprob()
        try:
            opt = input('Again? [y/n] '.lower())
            if opt and opt[0] == 'n':
                break
        except (KeyboardInterrupt, EOFError) as e:
            break

def print_name():
    print(__name__)

if __name__ == '__main__':
    main()

