=========================================================
《Python Cookbook》 3rd Edition 翻译 
=========================================================

-----------------
作者的话
-----------------
人生苦短，我爱Python！

笔者一直坚持使用Python3，因为它代表了Python的未来。虽然向后兼容是它的硬伤，但是这个局面迟早会改变的，
而且Python3的未来需要每个人的帮助和支持。
目前市面上的教程书籍，网上的手册大部分基本都是2.x系列的，专门基于3.x系列的书籍少的可怜。

最近看到一本《Python Cookbook》3rd Edition，完全基于Python3，写的也很不错。
为了Python3的普及，我也不自量力，想做点什么事情。于是乎，就有了翻译这本书的冲动了！
这不是一项轻松的工作，却是一件值得做的工作：不仅方便了别人，而且对自己翻译能力也是一种锻炼和提升。

后来想了下，一个人毕竟力量有限。如果能放到github上面来大家一起合作翻译，那效果就完全不一样了。
希望热爱python的有志之士可以一起合作把这本书翻译完成。通过fork/pull request方式。体验一把合作的魅力。
翻译这本书的前提是对python基础要有相当深入的研究，请不要使用google翻译这样的工具，
需要能把原文作者的意思完全表达出来，不需要逐字翻译，但表意一定要准确！

目前已经将项目的文件都已经新建好了，如果想参与进来，只需要更新对应的文件内容，然后pull request给我就行，
其他一切事情都由我来负责，也希望想参与进来的可以认真对待自己每一句的翻译，力求高质量。

译文中有什么错漏的地方请大家见谅，也欢迎大家指正： yidao620@gmail.com

--------------------------------------------------------------

++++++++
备注
++++++++
1. 原版PDF下载地址： http://pan.baidu.com/s/1dDhByJv
#. 所有文档均使用reStructuredText编辑，参考 reStructuredText_
#. 当前文档生成托管在 readthedocs_ 上
#. 生成的文档预览地址： python3-cookbook_
#. 使用了python官方文档主题 sphinx-rtd-theme_ ，也是默认的主题default.

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