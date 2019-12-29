#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 忽略大小写
Desc : 
"""
import re


def matchcase(word):
        def replace(m):
            text = m.group()
            if text.isupper():
                return word.upper()
            elif text.islower():
                return word.lower()
            elif text[0].isupper():
                return word.capitalize()
            else:
                return word
        return replace

def case_insens():
    text = 'UPPER PYTHON, lower python, Mixed Python'
    print(re.findall('python', text, flags=re.IGNORECASE))
    print(re.sub('python', 'snake', text, flags=re.IGNORECASE))

    # 大小写自动匹配
    print(re.sub('python', matchcase('snake'), text, flags=re.IGNORECASE))

if __name__ == '__main__':
    case_insens()
