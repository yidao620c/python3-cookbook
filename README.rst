=========================================================
《Python Cookbook》 3rd Edition 翻译 
=========================================================

在线预览地址： http://python3-cookbook.readthedocs.org/zh_CN/latest/

--------------------------------------------------------------

-----------------
译者的话
-----------------
人生苦短，我用Python！

译者一直坚持使用Python3，因为它代表了Python的未来。虽然向后兼容是它的硬伤，但是这个局面迟早会改变的，
而且Python3的未来需要每个人的帮助和支持。
目前市面上的教程书籍，网上的手册大部分基本都是2.x系列的，专门基于3.x系列的书籍少的可怜。

最近看到一本《Python Cookbook》3rd Edition，完全基于Python3，写的也很不错。
为了Python3的普及，我也不自量力，想做点什么事情。于是乎，就有了翻译这本书的冲动了！
这不是一项轻松的工作，却是一件值得做的工作：不仅方便了别人，而且对自己翻译能力也是一种锻炼和提升。

译者会坚持对自己每一句的翻译负责，力求高质量。但受能力限制，也难免有疏漏或者表意不当的地方。
如果译文中有什么错漏的地方请大家见谅，也欢迎大家随时指正： yidao620@gmail.com

--------------------------------------------------------------

++++++++
备注
++++++++
1. 原版PDF下载地址： http://pan.baidu.com/s/1dDhByJv
#. 所有文档均使用reStructuredText编辑，参考 reStructuredText_
#. 当前文档生成托管在 readthedocs_ 上
#. 生成的文档预览地址： python3-cookbook_
#. 使用了python官方文档主题 sphinx-rtd-theme_ ，也是默认的主题default.
#. 书中所有代码均在python 3.4版本下面运行通过，所有源码放在cookbook包下面

::

    # on_rtd is whether we are on readthedocs.org, this line of code grabbed from docs.readthedocs.org
    on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

    if not on_rtd:  # only import and set the theme if we're building docs locally
        import sphinx_rtd_theme
        html_theme = 'sphinx_rtd_theme'
        html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

    # otherwise, readthedocs.org uses their theme by default, so no need to specify it

.. _readthedocs: https://readthedocs.org/
.. _sphinx-rtd-theme: https://github.com/snide/sphinx_rtd_theme
.. _reStructuredText: http://docutils.sourceforge.net/docs/user/rst/quickref.html
.. _python3-cookbook: http://python3-cookbook.readthedocs.org/zh_CN/latest/

