#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 通过一个schema.sql来生成标准表结构的javabean
使用方法：python generate_javabean.py beans_dir package_name schema_name
"""
import sys
import os
import datetime

BASE_DOMAIN = """
_package_location_

import org.apache.commons.lang3.builder.ToStringBuilder;

import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import java.io.Serializable;
import java.util.Date;

/**
 * domain公共父类
 *
 * @author XiongNeng
 * @version 1.0
 * @since 2015/3/22
 */
public class BaseDomain implements Serializable {
    /**
     * 主键ID
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    /**
     * 创建时间
     */
    private Date createdTime;
    /**
     * 更新时间
     */
    private Date updatedTime;

    public String toString() {
        return ToStringBuilder.reflectionToString(this);
    }

    /**
     * 获取 更新时间.
     *
     * @return 更新时间.
     */
    public Date getUpdatedTime() {
        return updatedTime;
    }

    /**
     * 设置 创建时间.
     *
     * @param createdTime 创建时间.
     */
    public void setCreatedTime(Date createdTime) {
        this.createdTime = createdTime;
    }

    /**
     * 获取 创建时间.
     *
     * @return 创建时间.
     */
    public Date getCreatedTime() {
        return createdTime;
    }

    /**
     * 设置 更新时间.
     *
     * @param updatedTime 更新时间.
     */
    public void setUpdatedTime(Date updatedTime) {
        this.updatedTime = updatedTime;
    }

    /**
     * 设置 主键ID.
     *
     * @param id 主键ID.
     */
    public void setId(Long id) {
        this.id = id;
    }

    /**
     * 获取 主键ID.
     *
     * @return 主键ID.
     */
    public Long getId() {
        return id;
    }
}

"""

# 基类功能列
BASE_FIELS = {'id', 'updated_time', 'created_time'}

# MySQL type to java type
MYSQL_TYPE_MAP = {
    'BIT(1)': ('Boolean',)
    ,'BIT': ('byte[]',)
    ,'TINYINT': ('Integer',)
    ,'BOOLEAN': ('Boolean',)
    ,'BOOL': ('Boolean',)
    ,'SMALLINT': ('Integer',)
    ,'MEDIUMINT': ('Integer',)
    ,'INT': ('Integer',)
    ,'INTEGER': ('Integer',)
    ,'BIGINT': ('Long',)
    ,'FLOAT': ('Float',)
    ,'DOUBLE': ('Double',)
    ,'DECIMAL': ('BigDecimal', 'java.math.BigDecimal')
    ,'DATE': ('Date', 'java.util.Date')
    ,'DATETIME': ('Date', 'java.util.Date')
    ,'TIMESTAMP': ('Date', 'java.util.Date')
    ,'TIME': ('Date', 'java.util.Date')
    ,'CHAR': ('String ',)
    ,'VARCHAR': ('String',)
    ,'BINARY': ('byte[]',)
    ,'VARBINARY': ('byte[]',)
    ,'TINYBLOB': ('byte[]',)
    ,'TINYTEXT': ('String',)
    ,'BLOB': ('byte[]',)
    ,'TEXT': ('String',)
    ,'MEDIUMBLOB': ('byte[]',)
    ,'MEDIUMTEXT': ('String',)
    ,'LONGBLOB': ('byte[]',)
    ,'LONGTEXT': ('String',)
    ,'ENUM': ('String',)
    ,'SET': ('String',)
}

def camel_to_underline(camel_format):
    """
    驼峰命名格式转下划线命名格式
    """
    return ''.join([s if s.islower() else '_' + s.lower() for s in camel_format])[1:]


def underline_to_camel(underline_format, is_field=False):
    """
    下划线命名格式驼峰命名格式
    """
    try:
        result = ''.join([s.capitalize() for s in underline_format.split('_')])
    except:
        print(underline_format + "...error...")
    return result[0].lower() + result[1:] if is_field else result


def load_schema(filename):
    """先加载schema.sql文件来获取所有建表语句"""
    result = []
    with open(filename, encoding='utf-8') as sqlfile:
        each_table = []  # 每张表定义
        for line in sqlfile:
            if line.startswith('--'):
                temp_comment = line.split('--')[1].strip()
            elif 'DROP TABLE' in line:
                each_table.insert(0, temp_comment)
                each_table.insert(1, line.strip().split()[-1][:-1])
            elif ' COMMENT ' in line and 'ENGINE=' not in line:
                col_arr = line.split()
                col_name = col_arr[0]
                col_type = col_arr[1]
                if 'PRIMARY KEY' in line or 'NOT NULL' in line:
                    col_null = 'NOT NULL'
                else:
                    col_null = ''
                col_remark = line.split(' COMMENT ')
                cr = col_remark[-1].strip().replace("'", "")
                each_table.append((col_name, col_type, col_null, cr[:-1] if cr.endswith(',') else cr))
            elif 'ENGINE=' in line:
                # 单个表定义结束
                result.append(list(each_table))
                each_table.clear()
    return result


def write_beans(beans_dir, package_name, schema_name):
    # 今日格式化字符串
    today_str = ' * @since {}'.format(datetime.datetime.now().strftime('%Y/%m/%d'))
    # 先写BaseDomain.java
    with open(os.path.join(beans_dir, 'BaseDomain.java'), mode='w', encoding='utf-8') as jf:
        jf.write(BASE_DOMAIN.replace('_package_location_', 'package ' + package_name))
    table_data = load_schema(schema_name)
    for table in table_data:
        table_name_comment = table[0]
        table_name_real = table[1]
        class_name = underline_to_camel(table_name_real[2:])
        lines = []
        lines.append('package ' + package_name)
        lines.append('\n')
        lines.append('import javax.persistence.Table;')
        lines.append('\n')
        lines.append('/**')
        lines.append(' * ' + table_name_comment)
        lines.append(' *')
        lines.append(' * @author XiongNeng')
        lines.append(' * @version 1.0')
        lines.append(today_str)
        lines.append(' */')
        lines.append('@Table(name = "{}")'.format(table_name_real))
        lines.append('public class {} extends BaseDomain {{'.format(class_name))

        lines_fields = []
        lines_methods = []
        other_import = set()

        for each_column in table[2:]:
            # 列名
            column_name = each_column[0]
            if column_name in BASE_FIELS:
                continue
            field_name = underline_to_camel(column_name, is_field=True)
            field_name_method = underline_to_camel(column_name)
            # 类型
            ctype = each_column[1]
            java_type_t = MYSQL_TYPE_MAP[ctype.split('(')[0] if ctype != 'BIT(1)' else ctype]
            java_type = java_type_t[0]
            import_str = 'import {};'.format(java_type_t[1]) if len(java_type_t) > 1 else None
            # 空值约束
            column_null = each_column[2]
            # 字段生成
            column_comment = each_column[3]
            lines_fields.append('    /**')
            lines_fields.append('     * {}'.format(column_comment))
            lines_fields.append('     */')
            lines_fields.append('    private {} {};'.format(java_type, field_name))
            if import_str:
                other_import.add(import_str)

            # get方法生成
            lines_methods.append('    /**')
            lines_methods.append('     * 获取 {}.'.format(column_comment))
            lines_methods.append('     *')
            lines_methods.append('     * @return {}.'.format(column_comment))
            lines_methods.append('     */')
            lines_methods.append('    public {} get{}() {{'.format(java_type, field_name_method))
            lines_methods.append('        return {};'.format(field_name))
            lines_methods.append('    }')
            lines_methods.append('\n')
            # set方法生成
            lines_methods.append('    /**')
            lines_methods.append('     * 设置 {}.'.format(column_comment))
            lines_methods.append('     *')
            lines_methods.append('     * @param {} {}.'.format(field_name, column_comment))
            lines_methods.append('     */')
            lines_methods.append('    public void set{}({} {}) {{'.format(
                field_name_method, java_type, field_name))
            lines_methods.append('        this.{} = {};'.format(field_name, field_name))
            lines_methods.append('    }')
            lines_methods.append('\n')

        for each_other in other_import:
            lines.insert(2, each_other)

        lines.extend(lines_fields)
        lines.append('\n')
        lines.extend(lines_methods)
        lines.append('}')

        lines = [line + "\n" if line != '\n' else line for line in lines]
        # 开始写java源文件
        java_file = class_name + '.java'
        with open(os.path.join(beans_dir, java_file), mode='w', encoding='utf-8') as jf:
            jf.writelines(lines)


if __name__ == '__main__':
    # print(camel_to_underline("CompanyServiceImpl"))
    # print(underline_to_camel("company_service_impl", True))
    beans_dir = r'D:\work\zbeans\tobacco'
    package_name = r'com.cmback.tobacco.domain;'
    schema_name = r'D:\work\projects\gitprojects\tobacco\src\main\resources\sql\schema.sql'
    write_beans(beans_dir, package_name, schema_name)
    # write_beans(sys.argv[1], sys.argv[2], sys.argv[3])
    pass
