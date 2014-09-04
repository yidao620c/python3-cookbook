#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: str的translate方法清理文本
Desc : 
"""
import unicodedata
import sys


def clean_spaces(s):
    """普通替换使用replace最快"""
    s = s.replace('\r', '')
    s = s.replace('\t', ' ')
    s = s.replace('\f', ' ')
    return s


def translate_str():
    s = 'pýtĥöñ\fis\tawesome\r\n'
    print(s)

    remap = {
        ord('\t'): ' ',
        ord('\f'): ' ',
        ord('\r'): None  # Deleted
    }

    a = s.translate(remap)
    print(a)

    # 删除和音符
    cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode)
                             if unicodedata.combining(chr(c)))
    b = unicodedata.normalize('NFD', a)
    print(b)
    print(b.translate(cmb_chrs))

    # unicode数字字符映射到ascii字符
    digitmap = {c: ord('0') + unicodedata.digit(chr(c))
                for c in range(sys.maxunicode)
                if unicodedata.category(chr(c)) == 'Nd'}
    print(len(digitmap))
    x = '\u0661\u0662\u0663'
    print(x.translate(digitmap))

    # 先标准化，然后使用encode和decode函数
    b = unicodedata.normalize('NFD', a)
    print(type(b))
    print(b.encode('ascii', 'ignore').decode('ascii'))


if __name__ == '__main__':
    translate_str()

