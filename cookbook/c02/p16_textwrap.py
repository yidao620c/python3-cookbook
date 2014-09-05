#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 格式化字符串为指定宽度
Desc : 
"""
import textwrap
import os


def reformat_width():
    s = "Look into my eyes, look into my eyes, the eyes, the eyes, \
    the eyes, not around the eyes, don't look around the eyes, \
    look into my eyes, you're under."

    print(textwrap.fill(s, 70))
    print('*' * 40)
    print(textwrap.fill(s, 40))
    print('*' * 40)
    print(textwrap.fill(s, 40, initial_indent='    '))
    print('*' * 40)
    print(textwrap.fill(s, 40, subsequent_indent='    '))

    # 获取终端屏幕尺寸
    print(os.get_terminal_size().columns)


if __name__ == '__main__':
    reformat_width()