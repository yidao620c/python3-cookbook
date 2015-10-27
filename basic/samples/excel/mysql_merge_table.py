#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: mysql数据表结构和数据合并
Desc : 有两个表，航信CRM企业表t_crm_company，税局企业资料表t_tax_company，
现在需要将其记录合并，使用税号和名称组合来作为唯一性标识
"""
import sys
import copy

import logging
import datetime
import mysql.connector
from mysql.connector import errorcode
import traceback

# 查询航信CRM表
sql_select_taxcode_name = """
SELECT DISTINCT cust_tax_code,cust_name
FROM t_crm_company
WHERE update_time IS NULL OR update_time < '{}';
"""
# 通过税号和名称查询税局表中记录
sql_select_tax_info = """
SELECT
    legal_person,
    business_scope,
    reg_code,
    tax_number,
    cust_tax_name,
    addr,
    reg_type,
    tax_institution,
    duty,
    is_back_taxes,
    is_overdue,
    status,
    valid_st_date,
    qualification_nm,
    business,
    notes
FROM t_tax_company
WHERE cust_tax_code='{}' AND cust_name='{}' AND (notes is NULL OR notes<>'税号无效')
LIMIT 1;
"""
# 将税局的数据更新到航信表中
sql_update_crm = """
UPDATE t_crm_company
SET
   legal_person={},
   business_scope={},
   reg_code={},
   tax_number={},
   cust_tax_name={},
   addr={},
   reg_type={},
   tax_institution={},
   duty={},
   is_back_taxes={},
   is_overdue={},
   status={},
   valid_st_date={},
   qualification_nm={},
   business={},
   tax_notes={},
   update_time=now()
WHERE cust_tax_code='{}' AND cust_name='{}'
"""

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.FileHandler('d:/logs/merge_table.log', 'a', 'utf-8')])
_log = logging.getLogger('app.' + __name__)


def _connect():
    config = {
        'user': 'root',
        'password': 'mysql',
        'host': '183.232.56.59',
        'database': 'fastloan3',
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
            traceback.print_exc()
        if cnx:
            cnx.close()
    return cnx


def merge_table():
    conn_ = _connect()
    _log.info('---------------------------分割线-----------------------------')
    _log.info('数据库更新start')
    cursor = conn_.cursor()
    cursor.execute(sql_select_taxcode_name.format('2015-09-10 00:00:00'))
    code_names = [list(r) for r in cursor.fetchall()]
    _log.info("待更新数据量大小为：{}".format(len(code_names)))

    _log.info('合并企业资料start')
    for i, d2 in enumerate(code_names):
        try:
            cursor.execute(sql_select_tax_info.format(d2[0], d2[1]))
            each_record = cursor.fetchone()
            if each_record:
                u_list = [ "'{}'".format(r.replace("'", ";")) if r else 'null' for r in each_record]
                u_list.extend([d2[0], d2[1]])
                cursor.execute(sql_update_crm.format(*u_list))
        except:
            _log.error('--合并企业资料Exception,taxcode={},name={}--'.format(d2[0], d2[1]))
            traceback.print_exc()
            cursor.close()
            conn_.rollback()
            conn_.close()
            return
        if i % 50 == 0:
            _log.info("更新下标...i={}".format(i))
            conn_.commit()
    conn_.commit()
    _log.info('合并企业资料end')
    _log.info('数据库更新end')
    cursor.close()
    conn_.close()


if __name__ == '__main__':
    merge_table()
    pass
