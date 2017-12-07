=========================================================
《Python Cookbook》 3rd Edition 翻译 
=========================================================

-------------------------------------------------------------

《Python Cookbook》3rd 中文版3.0.0正式发布啦 ^_^！ ——2017/12/07

在线阅读地址： http://python3-cookbook.readthedocs.org/zh_CN/latest/

* 中文简体版PDF下载地址： https://pan.baidu.com/s/1sl3av3f
* 中文繁体版PDF下载地址： https://pan.baidu.com/s/1hsnJEpm

-------------------------------------------------------------

旧版本(2.0.0)下载

《Python Cookbook》3rd 中文版2.0.0正式发布啦 ^_^！ ——2016/03/31

* 中文简体版PDF下载地址： http://pan.baidu.com/s/1i4Jypff
* 中文繁体版PDF下载地址： http://pan.baidu.com/s/1i5k2CjN

-------------------------------------------------------------

++++++++++++++++
译者的话
++++++++++++++++
人生苦短，我用Python！

译者一直坚持使用Python3，因为它代表了Python的未来。虽然向后兼容是它的硬伤，但是这个局面迟早会改变的，
而且Python3的未来需要每个人的帮助和支持。
目前市面上的教程书籍，网上的手册大部分基本都是2.x系列的，专门基于3.x系列的书籍少的可怜。

最近看到一本《Python Cookbook》3rd Edition，完全基于Python3，写的也很不错。
为了Python3的普及，我也不自量力，想做点什么事情。于是乎，就有了翻译这本书的冲动了！
这不是一项轻松的工作，却是一件值得做的工作：不仅方便了别人，而且对自己翻译能力也是一种锻炼和提升。

译者会坚持对自己每一句的翻译负责，力求高质量。但受能力限制，也难免有疏漏或者表意不当的地方。
如果译文中有什么错漏的地方请大家见谅，也欢迎大家随时指正： yidao620@gmail.com

目前已经正式完成了整本书的翻译工作，历时1年多，不管怎样还是坚持下来了。现在共享给python社区。

--------------------------------------------------------------

++++++++++++++++
项目说明
++++++++++++++++
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


--------------------------------------------------------------


++++++++++++++++
其他贡献者
++++++++++++++++
1. Tony Yang (liuliu036@gmail.com)
2. Yu Longjun (https://github.com/yulongjun)
3. LxMit (https://github.com/LxMit)

-----------------------------------------------------

+++++++++++++++++++++
关于源码生成PDF文件
+++++++++++++++++++++

有网友提问怎样通过源码生成PDF文件，由于这个步骤介绍有点长，不适合放在README里面，
我专门写了篇博客专门介绍怎样通过ReadtheDocs托管文档，怎样自己生成PDF文件，大家可以参考一下。

https://www.xncoding.com/2017/01/22/fullstack/readthedoc.html

另外关于生成的PDF文件中会自动生成标题编号的问题，有热心网友也提出了解决方案，请参考issues108的解放方案：

https://github.com/yidao620c/python3-cookbook/issues/108

再次感谢每一位贡献者。

-----------------------------------------------------

+++++++++++++++++++
How to Contribute
+++++++++++++++++++

You are welcome to contribute to the project as follow

* fork project and commit pull requests
* add/edit wiki
* report/fix issue
* code review
* commit new feature
* add testcase

Meanwhile you'd better follow the rules below

* It's *NOT* recommended to submit a pull request directly to `master` branch. `develop` branch is more appropriate
* Follow common Python coding conventions
* Add the following [license] in each source file

++++++++++++++++
License
++++++++++++++++

(The Apache License)

Copyright (c) 2014-2015 `Xiong Neng <https://www.xncoding.com/>`_ and other contributors

Licensed under the Apache License, Version 2.0 (the "License"); 
you may not use this file except in compliance with the License. You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, 
software distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
See the License for the specific language governing permissions and limitations under the License.


.. _readthedocs: https://readthedocs.org/
.. _sphinx-rtd-theme: https://github.com/snide/sphinx_rtd_theme
.. _reStructuredText: http://docutils.sourceforge.net/docs/user/rst/quickref.html
.. _python3-cookbook: http://python3-cookbook.readthedocs.org/zh_CN/latest/

