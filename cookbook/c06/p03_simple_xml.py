#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 解析简单的XML
Desc : 
"""
from urllib.request import urlopen
from xml.etree.ElementTree import parse


def simple_xml():
    # Download the RSS feed and parse it
    u = urlopen('http://planet.python.org/rss20.xml')
    doc = parse(u)

    # Extract and output tags of interest
    for item in doc.iterfind('channel/item'):
        title = item.findtext('title')
        date = item.findtext('pubDate')
        link = item.findtext('link')

        print(title)
        print(date)
        print(link)
        print()

if __name__ == '__main__':
    simple_xml()

