#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: sample

    Filter(logname)，只允许来自logname或其子日志的消息通过
    app.net是app的子日志

    消息传播propagate和分层记录器：消息会传播给父记录器
    log.propagate属性获取是否传播标志

"""
import logging
import logging.handlers as handlers
import logging.config as config

__author__ = 'Xiong Neng'
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
# 模块基本用_，类级别用__
_log = logging.getLogger('app.' + __name__)


class FilterFunc(logging.Filter):
    def __init__(self, name):
        super().__init__()
        self.funcname = name

    def filter(self, record):
        if record.funcName == self.funcname: return False


def my_log():
    host = '10.0.0.175'
    port = 8080
    # 不要用 'xxxx' % (aa, bb)去手动格式化消息
    _log.error('error to connect to %s:%d', host, port)
    _log.addFilter(FilterFunc('foo'))  # 将忽略来自foo()函数的所有消息
    lgg = logging.getLogger('app.network.client')
    lgg.propagate = False  # 关闭传播属性
    lgg.error('do you see me?')  # 但是还是可以看到
    lgg.setLevel(logging.CRITICAL)
    lgg.error('now you see me?')
    logging.disable(logging.DEBUG)  # 全局关闭某个级别
    # 使用log配置文件，在main函数中执行一次即可
    config.fileConfig('applogcfg.ini')


if __name__ == '__main__':
    my_log()
