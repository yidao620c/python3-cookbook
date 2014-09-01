#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: 从一个网页中爬出所有的jpg格式的图片
    Desc : 
"""
import re
import urllib
import os

__author__ = 'Xiong Neng'


def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html


def getImg(html, pic_dir):
    reg = r'src="(http://.+?\.jpg)"\s+pic_ext='
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    if not pic_dir.endswith('/'):
        pic_dir += "/"
    if not os.path.exists(pic_dir):
        os.makedirs(pic_dir)
    count = 0
    for i in imglist:
        urllib.urlretrieve(i, '%spic_0%d.jpg' % (pic_dir, count))
        count += 1


def main():
    html = getHtml('http://tieba.baidu.com/p/2636927569')
    getImg(html, 'D:/libs/pics')


if __name__ == '__main__':
    main()
