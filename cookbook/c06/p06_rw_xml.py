#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 读取修改某个XML文档
Desc : 
"""
from xml.etree.ElementTree import parse, Element


def rw_xml():
    doc = parse('pred.xml')
    root = doc.getroot()
    # Remove a few elements
    root.remove(root.find('sri'))
    root.remove(root.find('cr'))
    # Insert a new element after <nm>...</nm>
    root.getchildren().index(root.find('nm'))

    e = Element('spam')
    e.text = 'This is a test'
    root.insert(2, e)
    # Write back to a file
    doc.write('newpred.xml', xml_declaration=True)



if __name__ == '__main__':
    rw_xml()



