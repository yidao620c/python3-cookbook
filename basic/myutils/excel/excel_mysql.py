#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 将航信excel表数据转换为MySQL中的数据
Desc : 
"""
import sys
import copy
from openpyxl import Workbook
from openpyxl import load_workbook

import logging
import datetime
import mysql.connector
from mysql.connector import errorcode

sql_create1 = """
    CREATE TABLE t_enterprise (
      id                  BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
      name                VARCHAR(100)  COMMENT '企业名称',
      tax_code           VARCHAR(30) COMMENT '税号',
      region_id          BIGINT COMMENT '区域ID',
      customer_type     INTEGER COMMENT '客户类型',
      enterprise_type   INTEGER COMMENT '企业类型',
      address            VARCHAR(200) COMMENT '详细地址',
      postcode           VARCHAR(10) COMMENT '邮编',
      tel                VARCHAR(50) COMMENT '联系电话',
      contact            VARCHAR(60) COMMENT '联系人',
      fax                VARCHAR(30) COMMENT '传真',
      mobile             VARCHAR(80) COMMENT '手机号',
      created_time      DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      updated_time      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT '企业表';
"""
sql_create2 = """
    CREATE TABLE t_region (
      id                 BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
      region_code       VARCHAR(16)  COMMENT '邮编',
      regian_name       VARCHAR(20) COMMENT '区域名',
      note               VARCHAR(200) COMMENT '备注',
      parent_id         BIGINT COMMENT '父级ID',
      created_time      DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      updated_time      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT '区域表';
"""
sql_insert_enterprise = """
    INSERT INTO t_enterprise
      (id,name,tax_code,region_id,customer_type,enterprise_type)
    VALUES (%s, %s, %s, %s, %s, %s);
"""
sql_update_enterprise = """
    UPDATE t_enterprise
    SET
        address=%s,
        postcode=%s,
        tel=%s,
        contact=%s,
        fax=%s,
        mobile=%s
    WHERE id=%s
"""
sql_insert_region = """
    INSERT INTO t_region
      (id,region_code,regian_name,note,parent_id)
    VALUES (%s, %s, %s, %s, %s);
"""
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.FileHandler('d:/logs/excel.log', 'a', 'utf-8')])
_log = logging.getLogger('app.' + __name__)


def _connect():
    config = {
        'user': 'root',
        'password': 'mysql',
        'host': '192.168.203.95',
        'database': 'hangxin',
        'raise_on_warnings': True,
    }
    cnx = None
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        if cnx:
            cnx.close()
    return cnx


def _init_table():
    conn_ = _connect()
    cursor = conn_.cursor()
    cursor.execute(sql_create1)
    cursor.execute(sql_create2)
    cursor.close()
    conn_.commit()
    conn_.close()


def parse_sheet(wb, sheet_name, column_num, log_msg):
    ws = wb[sheet_name]  # ws is now an IterableWorksheet
    result_list = []
    for row in ws.rows:
        row_data = []
        for i, cell in enumerate(row):
            if i >= column_num:
                break
            row_data.append(cell.value)
        result_list.append(row_data[:])
    _log.info(log_msg)
    return result_list


def handle_wrong_line(conn_, cursor_, wrong_line, ty=1):
    # 处理企业资料创建时的错误
    if ty == 1:
        id1 = wrong_line[0][0]
        many_data = wrong_line[0][1]
        next1 = wrong_line[1][0]
        next2 = wrong_line[1][1]
        next3 = wrong_line[1][2]
        many_data = many_data.replace('"', '')
        many_data = many_data.replace('_x000D_', '')
        many_list = [s.split() for s in many_data.split('\n') if s]
        many_list[0].insert(0, str(id1))
        many_list[-1][-1] = "{}{}".format(many_list[-1][-1], next1)
        many_list[-1].append(next2)
        many_list[-1].append(next3)
        # 扩充至指定的长度
        for many_item in many_list:
            if len(many_item) < 6:
                for i in range(6 - len(many_item)):
                    many_item.append(None)
        for i, v in enumerate([tuple(li) for li in many_list]):
            try:
                cursor_.execute(sql_insert_enterprise, v)
            except:
                conn_.rollback()
                logging.exception('handle_wrong_line哈企业资料Exception,line={}'.format(i))
                continue
            if i % 50 == 0:
                conn_.commit()
        conn_.commit()


def xlsx_to_table(xlsx_name):
    conn_ = _connect()
    _log.info('Excel文件解析start')
    wb = load_workbook(xlsx_name, read_only=True)
    # 先收集企业资料表
    list1 = parse_sheet(wb, 'customer', 6, 'customer表解析end')
    data1 = [(v[0], v[1], v[2], v[3], v[4], v[5]) for v in list1[1:]]
    # 收集地址和联系人表
    list2 = parse_sheet(wb, 'addr', 10, 'addr表解析end')
    data2 = [(v[2], v[4], v[5], v[6], v[7], v[8], v[0]) for v in list2[1:]]
    # 收集区域表
    list3 = parse_sheet(wb, 'region', 5, 'region表解析end')
    data3 = [(v[0], v[1], v[2], v[3], v[4]) for v in list3[1:]]
    _log.info('Excel文件解析end')
    _log.info('---------------------------分割线-----------------------------')
    _log.info('数据库更新start')
    cursor = conn_.cursor()
    _log.info('插入企业资料start')
    wrong1 = []
    find_large_name = False
    for i, d1 in enumerate(data1):
        if find_large_name:
            wrong1.append(d1)
            handle_wrong_line(conn_, cursor, wrong1)
            wrong1.clear()
            find_large_name = False
        try:
            cursor.execute(sql_insert_enterprise, d1)
        except:
            conn_.rollback()
            if len(str(d1[1])) > 600:
                logging.exception('-------插入企业资料Exception,line={}--------'.format(i))
                wrong1.append(d1)
                find_large_name = True
            continue
        if i % 50 == 0:
            conn_.commit()
    conn_.commit()
    _log.info('插入企业资料end')

    _log.info('更新企业联系信息start')
    for i, d2 in enumerate(data2):
        try:
            cursor.execute(sql_update_enterprise, d2)
        except:
            conn_.rollback()
            logging.exception('-------更新企业联系信息Exception,line={}-------'.format(i))
            handle_wrong_line(conn_, cursor,d2, ty=2)
        if i % 50 == 0:
            conn_.commit()
    conn_.commit()
    _log.info('插入企业资料表end')

    _log.info('插入区域信息start')
    for i, d3 in enumerate(data3):
        try:
            cursor.execute(sql_insert_region, d3)
        except:
            conn_.rollback()
            logging.exception('-------插入区域信息Exception,line={}-------'.format(i))
            handle_wrong_line(conn_, cursor, d3, ty=3)
        if i % 50 == 0:
            conn_.commit()
    conn_.commit()
    _log.info('插入区域信息end')

    _log.info('数据库更新end')
    cursor.close()
    conn_.close()


if __name__ == '__main__':
    excel = r'D:\download\20150505\gdc2.xlsx'
    _init_table()
    conn = _connect()
    xlsx_to_table(excel)
    pass
