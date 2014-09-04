#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: unicode字符串标准化表示
Desc : 
"""
import unicodedata


def nor_unicode():
    s1 = 'Spicy Jalape\u00f1o'
    s2 = 'Spicy Jalapen\u0303o'
    print(s1, s2)
    print(s1 == s2)
    print(len(s1), len(s2))

    # 先将文本标准化表示
    t1 = unicodedata.normalize('NFC', s1)
    t2 = unicodedata.normalize('NFC', s2)
    print(t1 == t2)
    print(ascii(t1))

    t3 = unicodedata.normalize('NFD', s1)
    t4 = unicodedata.normalize('NFD', s2)
    print(t3 == t4)
    print(ascii(t3))

    # 扩展的NFKC和NFKD
    s = '\ufb01'  # A single character
    print(s, len(s))
    print(unicodedata.normalize('NFD', s), len(unicodedata.normalize('NFD', s)))
    print(unicodedata.normalize('NFKC', s), len(unicodedata.normalize('NFKC', s)))
    print(unicodedata.normalize('NFKD', s), len(unicodedata.normalize('NFKD', s)))

    # 消除变音符
    t1 = unicodedata.normalize('NFD', s1)
    print(''.join(c for c in t1 if not unicodedata.combining(c)))


if __name__ == '__main__':
    nor_unicode()

