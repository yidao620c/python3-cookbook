# encoding: utf-8
"""
    Topic: sample
    Desc : 函数参数，可变长，命名参数
"""
__author__ = 'Xiong Neng'


def tupleVarArgs(arg1, arg2='defaultB', *theRest):
    """display regular args and non-keyword variable args"""
    print('format arg 1', arg1)
    print('format arg 2', arg2)
    for eachRestArg in theRest:
        print('each rest arg: ', eachRestArg)

# tupleVarArgs('abc')
# tupleVarArgs(23, 4.56)
# tupleVarArgs('abc', 123, 'xyz', 3456.33)


def tupleVarArgs2(arg1, arg2='defaultB', **theRest):
    """display regular args and non-keyword variable args"""
    print('format arg 1', arg1)
    print('format arg 2', arg2)
    for eachRestArg in theRest:
        print('each rest arg: key="%s",value="%s"' % (eachRestArg, theRest[eachRestArg]))


def main():
    tupleVarArgs('abc', 123, *('xyz', 3456.33))
    # tupleVarArgs2('abc')
    # tupleVarArgs2(23, 4.56)
    tupleVarArgs2('abc', www='xyz', yyy=3456.33, arg2=123)
    tupleVarArgs2('abc', arg2=123, **{'waht': '234r', 'bar': 123})
    darg = {'waht': '234r', 'bar': 123}
    tupleVarArgs2('abc', arg2=123, **darg)

if __name__ == '__main__':
    main()

