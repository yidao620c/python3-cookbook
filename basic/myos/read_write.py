#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc : 
"""
import re
import os
from os.path import join
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.FileHandler('d:/logs/cookbook.log', 'w', 'utf-8')])
_log = logging.getLogger('app.' + __name__)


def read_demo():
    """读取文本文件"""
    with open(r'D:\work\readme.txt', 'r', encoding='utf-8') as f:
        for line in f:
            print(line, end='')  # 这里必须用end=''，因为line里有换行，而print也会加换行
    with open(r'D:\work\readme.txt', 'ab+') as f:
        pass


def read_plus(txt_file, init_c, base_dir):
    """演示一下seek方法"""
    chapter = init_c - 1  # 章
    paper = 0  # 节
    write_file = None  # 接下来要写入的文件
    temp_lines = []  # 临时存放章或节内容
    with open(txt_file, mode='r', encoding='utf-8') as f:
        for line in f:
            if re.match('^CHAPTER \d+$', line.strip()):
                chapter += 1
                # 开始新的一章了
                _log.info('开始新的一章了，第{}章！'.format(chapter))
                # 前面的给写入文件中
                if temp_lines:
                    with open(write_file, mode='w', encoding='utf-8') as wf:
                        wf.writelines(temp_lines)
                    temp_lines.clear()
                # 首先创建一个章节源码目录
                c_dir = join(base_dir, 'cookbook', 'c{:02d}'.format(chapter))
                if not os.path.exists(c_dir):
                    os.makedirs(c_dir)
                # 找到章节文件
                chapters_dir = join(c_dir, 'source', 'chapters')
                onlyfiles = [join(chapters_dir, f) for f in os.listdir(chapters_dir)
                             if os.path.isfile(join(chapters_dir, f))]
                write_file = next(f for f in onlyfiles if f.startswith('p{:02d}'.format(chapter)))
            elif re.match('^{}.{}. '.format(chapter, paper + 1), line.strip()):
                f.seek(1, 1)  # 往前进一行
                if f.readline().strip() == 'Problem':
                    # 说明是新的一节开始了
                    paper += 1
                    f.seek(-1, 1)  # 退一行
                    _log.info('开始新的一节了，第{}章，第{}节！'.format(chapter, paper))
                    # 前面的给写入文件中
                    if temp_lines:
                        with open(write_file, mode='w', encoding='utf-8') as wf:
                            wf.writelines(temp_lines)
                        temp_lines.clear()
                    # 定义接下来要写入的节文件
                    paper_dir = join(base_dir, 'source', 'c{:02d}'.format(chapter))
                    pfs = [join(paper_dir, f) for f in os.listdir(paper_dir)
                                 if os.path.isfile(join(paper_dir, f))]
                    write_file = next(f for f in pfs if f.startswith('p{:02d}'.format(chapter)))
                else:
                    f.seek(-1, 1)
            else:
                temp_lines.append(line)


if __name__ == '__main__':
    print('{:02d}'.format(11))