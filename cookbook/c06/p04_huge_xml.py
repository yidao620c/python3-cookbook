#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 增量式的处理大型XML文档
Desc : 
"""
from xml.etree.ElementTree import iterparse
from xml.etree.ElementTree import parse
from collections import Counter


def parse_and_remove(filename, path):
    path_parts = path.split('/')
    doc = iterparse(filename, ('start', 'end'))
    # Skip the root element
    next(doc)

    tag_stack = []
    elem_stack = []
    for event, elem in doc:
        if event == 'start':
            tag_stack.append(elem.tag)
            elem_stack.append(elem)
        elif event == 'end':
            if tag_stack == path_parts:
                yield elem
                elem_stack[-2].remove(elem)
            try:
                tag_stack.pop()
                elem_stack.pop()
            except IndexError:
                pass


def huge_xml():
    potholes_by_zip = Counter()

    doc = parse('potholes.xml')
    for pothole in doc.iterfind('row/row'):
        potholes_by_zip[pothole.findtext('zip')] += 1
    for zipcode, num in potholes_by_zip.most_common():
        print(zipcode, num)


    potholes_by_zip = Counter()

    data = parse_and_remove('potholes.xml', 'row/row')
    for pothole in data:
        potholes_by_zip[pothole.findtext('zip')] += 1
    for zipcode, num in potholes_by_zip.most_common():
        print(zipcode, num)

if __name__ == '__main__':
    huge_xml()

