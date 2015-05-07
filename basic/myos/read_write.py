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


def convert_cookbook(txt_file, base_dir):
    """演示一下seek方法"""
    chapter = None      # 章
    paper = None        # 节
    write_file = None   # 接下来要写入的文件
    temp_lines = []     # 临时存放章或节内容
    hit_paper = False   # 是否命中小节标志
    hit_offset = 0      # 命中后行距
    with open(txt_file, mode='r', encoding='utf-8') as f:
        for line in f:
            c_match = re.match('^CHAPTER (\d+)$', line.strip())
            p_match = re.match('^(\d+)\.(\d+)\. ', line.strip())
            a_match = re.match('^APPENDIX A$', line.strip())
            if c_match:
                old_chapter = chapter
                chapter = int(c_match.group(1))
                if old_chapter and chapter - old_chapter != 1:
                    _log.error('章节不连续啊: {}'.format(line.strip()))
                    continue
                # 开始新的一章了
                _log.info('------------------------------------------------------')
                _log.info('---------开始新的一章了，第{}章！-----------'.format(chapter))
                # 前面的给写入文件中
                if temp_lines:
                    _log.info('write_file={}'.format(write_file))
                    with open(write_file, mode='r', encoding='utf-8') as wf:
                        for i in range(7):
                            temp_lines.insert(i, wf.readline())
                    with open(write_file, mode='w', encoding='utf-8') as wf:
                        wf.writelines(temp_lines)
                    temp_lines.clear()
                # 首先创建一个章节源码目录
                c_dir = join(base_dir, 'cookbook', 'c{:02d}'.format(chapter))
                if not os.path.exists(c_dir):
                    os.makedirs(c_dir)
                # 找到章节文件
                chapters_dir = join(base_dir, 'source', 'chapters')
                onlyfiles = [f for f in os.listdir(chapters_dir)
                             if os.path.isfile(join(chapters_dir, f))]
                write_file = next(join(chapters_dir, f) for f in onlyfiles if
                                  f.startswith('p{:02d}'.format(chapter)))
                _log.info('找到章节文件:{}'.format(write_file))
            elif p_match:
                hit_paper = True
                paper = int(p_match.group(2))
                hit_offset = 0
            elif hit_paper and hit_offset <= 2:
                if line.strip() == 'Problem':
                    # 说明是新的一节开始了
                    _log.info('开始新的一节了，第{}章，第{}节！'.format(chapter, paper))
                    # 前面的给写入文件中
                    if temp_lines:
                        if 'chapters' not in write_file:
                            _log.info('write_file={}'.format(write_file))
                            with open(write_file, mode='r', encoding='utf-8') as wf:
                                for i in range(7):
                                    temp_lines.insert(i, wf.readline())
                            with open(write_file, mode='w', encoding='utf-8') as wf:
                                wf.writelines(temp_lines)
                        temp_lines.clear()
                    # 定义接下来要写入的节文件
                    paper_dir = join(base_dir, 'source', 'c{:02d}'.format(chapter))
                    pfs = [f for f in os.listdir(paper_dir)
                           if os.path.isfile(join(paper_dir, f))]
                    write_file = next(
                        join(paper_dir, f) for f in pfs if f.startswith('p{:02d}'.format(paper)))
                    _log.info('下次要写的小节文件:{}'.format(write_file))
                    # 创建小节源码文件
                    c_dir = join(base_dir, 'cookbook', 'c{:02d}'.format(chapter))
                    with open(join(c_dir, 'p{:02d}_.py'.format(paper)), 'w',
                              encoding='utf-8') as pfile:
                        pfile.write('#!/usr/bin/env python\n')
                        pfile.write('# -*- encoding: utf-8 -*-\n')
                        pfile.write('"""\n')
                        pfile.write('Topic: \n')
                        pfile.write('Desc : \n')
                        pfile.write('"""\n')
                    hit_paper = False
                hit_offset += 1
                if hit_offset > 2:
                    hit_paper = False
            elif a_match:
                # 前面的给写入文件中
                if temp_lines:
                    _log.info('write_file={}'.format(write_file))
                    with open(write_file, mode='r', encoding='utf-8') as wf:
                        for i in range(7):
                            temp_lines.insert(i, wf.readline())
                    with open(write_file, mode='w', encoding='utf-8') as wf:
                        wf.writelines(temp_lines)
                    temp_lines.clear()
            else:
                temp_lines.append(line)


if __name__ == '__main__':
    convert_cookbook(r'D:\download\20150430\pc_after.txt'
                     , r'D:\work\projects\gitprojects\python3-cookbook')
