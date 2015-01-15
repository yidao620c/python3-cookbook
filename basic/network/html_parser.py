#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: sample
    Desc : 
"""
from html.parser import HTMLParser

import re
from urllib.request import Request, urlopen


class Parselinks(HTMLParser):
    def __init__(self):
        self.data = []
        self.href = 0
        self.linkname = ''
        self.patt = re.compile(r'^/doc/\d+$')
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href' and re.match(self.patt, value):
                    self.href = 1
                    self.data.append([value])

    def handle_data(self, data):
        if self.href:
            self.linkname += data

    def handle_endtag(self, tag):
        if tag == 'a' and self.href:
            self.linkname = ''.join(self.linkname.split())
            self.linkname = self.linkname.strip()
            self.data[-1].append(self.linkname)
            self.linkname = ''
            self.href = 0


class ParsePages(HTMLParser):
    def __init__(self):
        self.data = set([])
        self.href = 0
        self.patt = re.compile(r'^\?p=\d+$')
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href' and re.match(self.patt, value):
                    self.href = 1
                    self.data.add(value)

    def handle_endtag(self, tag):
        if tag == 'a' and self.href:
            self.href = 0


def fetch_data(pparser, url):
    headers = {
        'User-Agent': '''Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)
                Chrome/28.0.1500.72 Safari/537.36'''
    }
    req = Request(
        url=url,
        headers=headers
    )
    pparser.feed(urlopen(req).read())
    pparser.close()
    return pparser.data


def main():
    result = []
    pattt = re.compile(r'程序员编码诀窍')
    urll = 'http://www.oschina.network/doc'
    pages = fetch_data(ParsePages(), urll)
    for eachurl in pages:
        print('**********')
        each_page_data = fetch_data(Parselinks(), urll + eachurl)
        for each_link_data in each_page_data:
            if re.match(pattt, each_link_data[1]):
                result.append(each_link_data)

    print("*" * 30)
    for r in result:
        print('%s -> %s' % tuple(r))


if __name__ == '__main__':
    main()