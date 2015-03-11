#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 通过一个schema.sql来生成excel表格的数据库设计文档
Desc : 
"""
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter
from openpyxl.drawing import Image
from openpyxl.writer.dump_worksheet import WriteOnlyCell
from openpyxl.comments import Comment
from openpyxl.styles import Style, PatternFill, Border, Side, Alignment, Protection, Font


def load_xlsx():
    wb = Workbook()
    ws = wb.active
    ws.title = "首页列表"
    ws = wb['首页列表']
    print(wb.get_sheet_names())
    print(ws['D5'], ws.cell(row=5, column=4))
    cell_range = ws['A1':'C2']

    wb2 = load_workbook('D:/work/MySQL数据库表.xlsx')
    print(wb2.get_sheet_names())


def write_xlsx():
    wb = Workbook()
    dest_filename = 'empty_book.xlsx'
    ws = wb.active
    ws.title = "首页列表"
    for col_idx in range(1, 10):
        col = get_column_letter(col_idx)
        for row in range(1, 20):
            ws['%s%s' % (col, row)].value = '%s%s' % (col, row)
    ws.merge_cells('A1:B1')  # 合并单元格
    ws.unmerge_cells('A1:B1')
    ws = wb.create_sheet()
    ws.title = 'Pi'
    ws['F5'] = 3.14
    # img = Image('logo.png')
    # img.drawing.top = 100
    # img.drawing.left = 150

    wb.save(filename=dest_filename)

    wb = load_workbook(filename='empty_book.xlsx')
    sheet_ranges = wb['首页列表']
    print(sheet_ranges['D18'].value)


def write_only():
    wb = Workbook()
    ws = wb.create_sheet()
    ws.title = "首页列表"
    c = ws['A1']
    c.style = Style(font=Font(name='Courrier', size=36)
                    , fill=PatternFill(fill_type=None, start_color='FFFFFFFF',
                                       end_color='FF000000')
                    , protection=Protection(locked='inherit', hidden='inherit')
                    , alignment=Alignment(horizontal='general', vertical='bottom',
                                          shrink_to_fit=True)
                    , border=Border(left=Side(border_style=None, color='FF000000')))
    c.value = '姓名'
    # cell = WriteOnlyCell(ws, value="hello world")
    # cell.style = Style(font=Font(name='Courrier', size=36))
    # cell.comment = Comment(text="A comment", author="Author's Name")

    # ws.header_footer.center_header.text = 'My Excel Page'
    # ws.header_footer.center_header.font_size = 14
    # ws.header_footer.center_header.font_name = "Tahoma,Bold"
    # ws.header_footer.center_header.font_color = "CC3366"
    wb.save(filename='empty_book.xlsx')


def load_schema(filename):
    """先加载schema.sql文件来获取所有建表语句"""
    result = []
    with open(filename, encoding='utf-8') as sqlfile:
        each_table = []  # 每张表定义
        for line in sqlfile:
            if line.startswith('--'):
                each_table.insert(0, line.split('--')[1].strip())
            elif ' COMMENT ' in line and 'ENGINE=' not in line:
                col_arr = line.split()
                col_name = col_arr[0]
                col_type = col_arr[1]
                if 'PRIMARY KEY' in line or 'NOT NULL' in line:
                    col_null = 'NOT NULL'
                else:
                    col_null = ''
                col_remark = col_arr[-1]
                each_table.append((col_name, col_type, col_null, col_remark))
            elif 'ENGINE=' in line:
                # 单个表定义结束
                result.append(list(each_table))
                each_table.clear()
    return result


def write_dest(xlsx_name, schema_name):
    table_data = load_schema(schema_name)
    wb = Workbook()
    wb.active.title = "首页列表"
    for table in table_data:
        ws = wb.create_sheet(title=table[0])
        ws.merge_cells('E3:H3')  # 合并单元格
        ws['E3'] = table[0]
        ws['E5'] = '列名'
        ws['F5'] = '类型'
        ws['G5'] = '空值约束'
        ws['H5'] = '备注'
        for idx, each_column in enumerate(table[1:]):
            ws['E{}'.format(idx + 6)] = each_column[0]
            ws['F{}'.format(idx + 6)] = each_column[1]
            ws['G{}'.format(idx + 6)] = each_column[2]
            ws['H{}'.format(idx + 6)] = each_column[3].strip().split('\'')[1]
    wb.save(filename=xlsx_name)


if __name__ == '__main__':
    # write_xlsx()
    # write_only()
    write_dest('aaa.xlsx', 'schema.sql')
    pass
