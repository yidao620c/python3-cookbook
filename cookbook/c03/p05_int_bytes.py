#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 大整数与字节的相互转换
Desc : 
"""


def int_bytes():
    data = b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'
    print(len(data))
    print(int.from_bytes(data, 'little'))
    print(int.from_bytes(data, 'big'))

    x = 94522842520747284487117727783387188
    print(x.to_bytes(16, 'big'))
    print(x.to_bytes(20, 'big'))


    # bit_length真有用
    x = 523 ** 23
    print(x)
    print(x.bit_length())
    nbytes, rem = divmod(x.bit_length(), 8)
    if rem:
        nbytes += 1
    print(x.to_bytes(nbytes, 'little'))

if __name__ == '__main__':
    int_bytes()

