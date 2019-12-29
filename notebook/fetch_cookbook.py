#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Seaky
# @Date:   2019/6/19 14:40

# pip install requests beautifulsoup4

import json
import re
from copy import deepcopy
from pathlib import Path

import requests
from bs4 import BeautifulSoup

TEMPLATE = {
    "cells": [],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.7.1"
        },
        "toc": {
            "base_numbering": 1,
            "nav_menu": {},
            "number_sections": True,
            "sideBar": True,
            "skip_h1_title": True,
            "title_cell": "Table of Contents",
            "title_sidebar": "Contents",
            "toc_cell": False,
            "toc_position": {},
            "toc_section_display": True,
            "toc_window_display": True
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}


class Chapter:
    def __init__(self, chapter_address):
        self.chapter_address = chapter_address
        self.path = re.sub('/[^/]+?$', '/', chapter_address)
        self.ss = requests.session()

    def fetch(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        print(url)
        raw = self.ss.get(url, headers=headers).content
        m = re.search('charset=\W*(?P<charset>\w+)', raw[:200].decode(errors='ignore'))
        charset = m.groupdict().get('charset', 'utf-8')
        if charset == 'gb2312':
            charset = 'cp936'
        return raw.decode(encoding=charset)

    def fetch_list(self):
        content = self.fetch(self.chapter_address)
        soup = BeautifulSoup(content, 'html.parser')
        self.chapter_title = soup.find('h1').text.replace('¶', '')
        self.chapter_desc = soup.find('p').text
        self.sections = []
        for x in soup.find_all('a', class_='reference internal', href=re.compile('/p\d+_')):
            if x['href'] not in self.sections:
                self.sections.append(x['href'])

    def fetch_sections(self, sep=False):
        cells = [{
            "cell_type": "markdown",
            "metadata": {},
            "source": ['# {}\n {}'.format(self.chapter_title, self.chapter_desc)]
        }]
        dpath = Path('ipynb')
        dpath.mkdir(exist_ok=True)
        for href in self.sections[:]:
            _cells = self.fetch_content(self.path + href)
            if sep:
                _dpath = dpath / self.chapter_title
                _dpath.mkdir(exist_ok=True)
                TEMPLATE['cells'] = _cells
                *_, section_name = href.split('/')
                open(str(_dpath / '{}.ipynb'.format(section_name.split('.')[0])), 'w').write(json.dumps(TEMPLATE, indent=2))
            cells.extend(_cells)
        TEMPLATE['cells'] = cells
        open(str(dpath / '{}.ipynb'.format(self.chapter_title)), 'w').write(json.dumps(TEMPLATE, indent=2))

    def fetch_content(self, url):
        content = self.fetch(url)
        soup = BeautifulSoup(content, 'html.parser')

        cell_markdown = {
            "cell_type": "markdown",
            "metadata": {},
            "source": []
        }
        cell_code = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": []
        }
        cells = []
        p_header = re.compile('^h(?P<level>\d)$')
        for tag in [x for x in soup.descendants if x.name]:
            if p_header.search(tag.name):
                cell = deepcopy(cell_markdown)
                cell['source'].append(
                    '{} {}\n'.format('#' * (int(p_header.search(tag.name).group('level')) + 1), tag.text))
                cells.append(cell)
            elif tag.name == 'p':
                if 'Copyright' in tag.text:
                    continue
                cell = deepcopy(cell_markdown)
                cell['source'].append(tag.text)
                cells.append(cell)
            elif tag.name == 'pre':
                if '>>>' not in tag.text:
                    # code
                    source = [re.sub('(^\n*|\n*$)', '', tag.text)]
                else:
                    # idle
                    source = []
                    for line in tag.text.split('\n'):
                        if re.search('^(>|\.){3}', line):
                            if re.search('^(>|\.){3}\s*$', line):
                                continue
                            source.append(re.sub('^(>|\.){3} ', '', line))
                        else:
                            if source:
                                cell = deepcopy(cell_code)
                                cell['source'].append(re.sub('(^\n*|\n*$)', '', '\n'.join(source)))
                                cells.append(cell)
                                source = []
                            else:
                                continue
                if source:
                    cell = deepcopy(cell_code)
                    cell['source'].append('\n'.join(source))
                    cells.append(cell)
        for cell in cells:
            for i, text in enumerate(cell['source']):
                cell['source'][i] = text.replace('¶', '')
        return cells


def fetch_all(sep=False):
    content = requests.get('https://python3-cookbook.readthedocs.io/zh_CN/latest/').content
    soup = BeautifulSoup(content)
    for x in soup.find_all('a', class_='reference internal', href=re.compile('chapters/p\d+'))[2:15]:
        ch = Chapter('https://python3-cookbook.readthedocs.io/zh_CN/latest/' + x['href'])
        ch.fetch_list()
        ch.fetch_sections(sep=sep)


if __name__ == '__main__':
    # ch = Chapter('https://python3-cookbook.readthedocs.io/zh_CN/latest/chapters/p01_data_structures_algorithms.html')
    # ch.fetch_list()
    # ch.fetch_sections()
    fetch_all(sep=True)
