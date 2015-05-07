#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Desc: 如何将原有的《Python Cookbook》3rd edition.pdf文件转换为我自己的cookbook翻译项目格式

1. 首先使用在线PDF文件切割截取出自己想要的pdf文件部分：http://smallpdf.com/split-pdf
2. 安装PDFMiner依赖，然后使用：pdf2txt.py -o pc.txt /home/mango/work/perfect.pdf生成的txt文件
3. 把生成的txt文件放到idea中，去除某些没用的符号，比如'口'字符，全局replace
4. 调用beauty2()函数，去除了页头和页脚的部分
5. 调用convert_cookbook()函数将txt文件转换为cookbook项目所需的格式
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


def beauty(txt_file):
    with open(txt_file, mode='r+', encoding='utf-8') as f:
        lines = f.readlines()
        f.seek(0)
        for line in lines:
            if line.startswith('www.it-ebooks.info'):
                f.seek(f.tell() - 1, 1)
                if f.readline().startswith('Chapter '):
                    # 回退7位
                    f.seek(f.tell() - 7, 1)
                else:
                    f.seek(f.tell() - 5, 1)
            else:
                f.write(line)
        f.truncate()


def beauty2(pre_txt, after_txt):
    with open(pre_txt, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
    result_lines = []
    for i, line in enumerate(lines):
        if line.startswith('www.it-ebooks.info'):
            if result_lines[len(result_lines) - 4].startswith('| '):
                # 删除7
                for k in range(7):
                    result_lines.pop()
            else:
                check_str = result_lines[len(result_lines) - 2].strip()
                if re.match('\d{3}', check_str):
                    # 删除3行
                    for k in range(3):
                        result_lines.pop()
        else:
            result_lines.append(line)

    # 结果写入
    with open(after_txt, mode='w', encoding='utf-8') as f:
        f.writelines(result_lines)


def convert_cookbook(txt_file, base_dir):
    """演示一下seek方法"""
    chapter = None  # 章
    paper = None  # 节
    write_file = None  # 接下来要写入的文件
    temp_lines = []  # 临时存放章或节内容
    hit_paper = False  # 是否命中小节标志
    hit_offset = 0  # 命中后行距
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
            elif re.match('^Solution$', line.strip()):
                temp_lines.append('|\n')
                temp_lines.append('\n')
                temp_lines.append('----------\n')
                temp_lines.append('解决方案\n')
                temp_lines.append('----------\n')
            elif re.match('^Discussion$', line.strip()):
                temp_lines.append('|\n')
                temp_lines.append('\n')
                temp_lines.append('----------\n')
                temp_lines.append('讨论\n')
                temp_lines.append('----------\n')
            else:
                temp_lines.append(line)


if __name__ == '__main__':
    convert_cookbook(r'D:\download\20150430\pc_after.txt'
                     , r'D:\work\projects\gitprojects\python3-cookbook')
