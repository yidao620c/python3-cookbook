#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 编码/解码Base64
Desc : 
"""
import base64


def codec_base64():
    s = b'hello'

    # Encode as Base64
    a = base64.b64encode(s)
    print(a)

    # Decode from Base64
    b = base64.b64decode(a)
    print(b)

if __name__ == '__main__':
    codec_base64()


