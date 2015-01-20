#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: sample
    Desc : 
"""
import optparse
__author__ = 'Xiong Neng'

def demo():
    p = optparse.OptionParser()
    # 简单选项，不带参数
    p.add_option('-t', action='store_true', dest='tracing')
    # 接受字符串参数
    p.add_option('-o', '--outfile', action='store', type='string', dest='outfile')
    # 需要整数参数
    p.add_option('-d', '--debuglevel', action='store', type='int', dest='debug')
    # 带一些选择的选项
    p.add_option('--speed', action='store', type='choice', dest='speed',
                 choices=['slow', 'fast', 'ludicrous'])
    # 带多个参数选项
    p.add_option('--coord', action='store', type='int', dest='coord', nargs=2)
    # 一组控制常用目的地的选项，不带参数，将const的值保存到dest指定的变量中
    p.add_option('--novice', action='store_const', const='novice', dest='mode')
    p.add_option('--guru', action='store_const', const='guru', dest='mode')

    # 为各个选项dest设置默认值
    p.set_default(tracing=False,
                  debug=0,
                  speed='fast',
                  coord=(0,0))

    # 开始解析参数
    opt, args = p.parse_args()

    # 打印参数
    print('tracing=', opt.tracing)
    print('outfile=', opt.outfile)
    print('debug=', opt.debug)
    print('speed=', opt.speed)
    print('coord=', opt.coord)
    print('mode=', opt.mode)

    # 打印余下的
    print('args=', args)

    pass

if __name__ == '__main__':
    pass
