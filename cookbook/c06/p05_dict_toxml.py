#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 字典转换成XML格式
Desc : 
"""
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring


def dict_to_xml(tag, d):
    """
    Turn a simple dict of key/value pairs into XML
    """
    elem = Element(tag)
    for key, val in d.items():
        child = Element(key)
        child.text = str(val)
        elem.append(child)
    return elem

if __name__ == '__main__':
    r = dict_to_xml('root', {'1':'22', '3':'444'})
    print(r)
    print(tostring(r))
    r.set('_id','1234')
    print(tostring(r))



