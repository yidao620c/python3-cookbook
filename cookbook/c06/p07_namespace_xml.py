#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 处理含命名空间的XML文档
Desc : 
"""


class XMLNamespaces:
    def __init__(self, **kwargs):
        self.namespaces = {}
        for name, uri in kwargs.items():
            self.register(name, uri)

    def register(self, name, uri):
        self.namespaces[name] = '{' + uri + '}'

    def __call__(self, path):
        return path.format_map(self.namespaces)


if __name__ == '__main__':
    ns = XMLNamespaces(html='http://www.w3.org/1999/xhtml')
    # doc.find(ns('content/{html}html'))
    # doc.findtext(ns('content/{html}html/{html}head/{html}title'))