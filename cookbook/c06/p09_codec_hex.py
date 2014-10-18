#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 编码/解码十六进制原始字符串
Desc : 
"""
import binascii
import base64


def codec_hex():
    s = b'hello'
    # Encode as hex
    h = binascii.b2a_hex(s)
    print(h)
    # Decode back to bytes
    h = binascii.a2b_hex(h)
    print(h)

    # 使用base64模块也可以
    h = base64.b16encode(s)
    print(h)
    print(h.decode('ascii'))
    h = base64.b16decode(h)
    print(h)
    print(h.decode('ascii'))


if __name__ == '__main__':
    codec_hex()
