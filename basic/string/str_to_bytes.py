#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Function:
【整理】Python中字符编码的总结和对比

Python 3.x中，直接输出的字符串（被单引号或双引号括起来的），就已经是Unicode类型的str了。
当然，有一些前提：
1. Python文件开始已经声明对应的编码
2. Python文件本身的确是使用该编码保存的
3. 两者的编码类型要一样（比如都是UTF-8或者都是GBK等）
这样Python解析器，才能正确的把你所输出字符串，解析为对应的unicode的str

Author:     Xiong Neng
Verison:    2014-09-25
-------------------------------------------------------------------------------
"""


def str_to_bytes():
    """Demo Python 3.x (unicode) str to bytes
    """
    zhcn_unicode = """
    1.此处的，Python 3.x中，默认字符串的写法，就已经是unicode类型的字符串了。
    2.当然，还是有一点前提的，那就是:
    (1)此处python文件所指定的编码类型
    (2)要和你当前python文件实际所采用的编码类型，要匹配和一致，
    即此处，两者均是UTF-8，所以，Python解析器，才能正确的将我们此处所输入的UTF-8的中文字符，
    正确地解码为对应的Unicode字符串的；
    3.接下来将要演示的是，打印对于的此处字符的类型；
    然后再直接输出显示到windows的GBK编码的cmd中
    """
    print("type(zhcn_unicode)=", type(zhcn_unicode))  # type(zhcn_unicode)= <class 'str'>
    print(zhcn_unicode)
    zhcn_gbk_bytes = zhcn_unicode.encode("GBK")
    # print("You should see these zh-CN bytes in windows cmd normally,"
    #       " which begin with b preffix: zhcnGbkBytes=%s" % (zhcn_gbk_bytes))
    print('中'.encode('UTF-8'))  # UTF-8的中文3个字节，输出 b'\xe4\xb8\xad'
           # You should see these zh-CN bytes in windows cmd normally,
           # which begin with b preffix:
           # zhcnGbkBytes=b'1.\xb4\xcb\xb4\xa6\xb5 ...... \xc2\xeb\xb5\xc4cmd\xd6\xd0'


def bytes_to_str():
    """Demo Python 3.x bytes to (unicode) str
    """

    #此处的bytes，只能接受ASCII字符
    #想要输入非ASCII的字符，则只能通过\xYY的十六进制方式输入，其中YY为对应的16进制的值
    #此处，我是已经在别处，通过把对应的中文:
    #"1.Python 3.x中，给字符串前面添加字母b，表示是bytes的字符串；
    # 2.此处之所以可以实现，接下来的，Python解析器，可以正确的将bytes解码为Unicode的str，那是因为
    #     (1)此处python文件所指定的编码类型
    #     (2)要和你当前python文件实际所采用的编码类型，是一致的，都是UTF-8；
    # 3.接下来将要演示的是，将此bytes字符串，解码为Unicode的str，
    # 然后在此处的终端，windows的默认编码为GBK的cmd中显示出来；";

    #解析为UTF-8的bytes了，所以下面你看到的是，解析后的，一堆bytes
    zhcnBytes = b"1.\xe6\xad\xa4\xe5\xa4\x84\xe7\x9a\x84\xef\xbc\x8cPython 3.x"
    print("type(zhcnBytes)=",type(zhcnBytes))  # type(zhcnBytes)= <class 'bytes'>
    zhcnUnicodeStr = zhcnBytes.decode("UTF-8")
    print("zh-CN unicode str in windows cmd normally: zhcnUnicodeStr=%s"%(zhcnUnicodeStr))
    # zh-CN unicode str in windows cmd normally: zhcnUnicodeStr=
    # 1.此处的，Python 3.x中 ...... 然后再直接输出显示到windows的GBK编码的cmd中

if __name__ == "__main__":
    str_to_bytes()