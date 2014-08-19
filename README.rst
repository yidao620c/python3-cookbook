=========================================================
《Python Cookbook 3rd Edition》 翻译 
=========================================================

刚接触到《Python Cookbook 3rd Edition》这本书时，它还没有相应的中文版。
在阅读这本书时，突然想到：为什么把它不翻译出来也方便别人阅读呢？于是决定在阅读时逐章地翻译这本书。
这不是一项轻松的工作，却是一件值得做的工作：不仅方便了别人，而且对自己翻译能力也是一种锻炼和提升。

后来想了下，一个人毕竟力量有限。如果能放到github上面来大家一起合作翻译，那效果就完全不一样了。
希望热爱python的有志之士可以一起合作把这本书翻译完成。通过fork/pull request方式。体验一把合作的魅力。
翻译这本书的前提是对python基础要有相当深入的研究，请不要使用google翻译这样的工具，
需要能把原文作者的意思完全表达出来，不需要逐字翻译，但表意一定要准确！

本书在翻译时遵循一条原则，就是通过查阅《Python3.4.0用户手册》在完全读懂文字和代码后再翻译，
而不是仅仅根据文字翻译，这样翻译和作者要表达的意思会更加接近并且更加容易理解。
原书正文之前除了作者简介以外的那些对于阅读没多大帮助的信息留到最后一章翻译完成后再翻译补齐。

目前翻译了第一章——数据结构与算法 ，感觉到如果对Python标准库一无所知，
读起来不会很容易。所以建议您在阅读时，最好也了解一下手册中相关的地方。

译文中有什么错漏的地方请大家见谅，也欢迎大家指正： yidao620@gmail.com

--------------------------------------------------------------

注：

1. 所有文档均使用reStructuredText编辑，参考 reStructuredText_
2. 当前文档生成托管在 readthedocs_ 上
3. 使用了python官方文档主题 sphinx-rtd-theme_

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