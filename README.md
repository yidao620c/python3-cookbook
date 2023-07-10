[![GitHub issues](https://img.shields.io/github/issues/yidao620c/python3-cookbook.svg)](https://github.com/yidao620c/python3-cookbook/issues)
[![License][licensesvg]][license]
[![Github downloads](https://img.shields.io/github/downloads/yidao620c/python3-cookbook/total.svg)](https://github.com/yidao620c/python3-cookbook/releases/latest)
[![GitHub release](https://img.shields.io/github/release/yidao620c/python3-cookbook.svg)](https://github.com/yidao620c/python3-cookbook/releases)

# Python Cookbook 3rd Edition 中文翻译 

_Python Cookbook_ 3rd Edition 中文版正式发布啦 ^_^！ —— 2017/12/07

在线阅读地址：<http://python3-cookbook.readthedocs.org/zh_CN/latest/>

最新版（3.0.0）下载

* 简体中文版 PDF 下载地址：<https://pan.baidu.com/s/1pL1cI9d>
* 繁体中文版 PDF 下载地址：<https://pan.baidu.com/s/1qX97VJI>

## 关于作者 David Beazley

本书作者是 David Beazley 大神，一位独立的计算机科学家、教育家，以及有着 35 年开发经验的软件开发者。
他在 Python 社区一直都很活跃，编写了很多的 [Python 包](http://www.dabeaz.com/software.html)，
发表了很多的公开[演讲视频](http://www.dabeaz.com/talks.html) 以及 
[编程教程](http://www.dabeaz.com/tutorials.html)。
同时还是 [Python Essential Reference](http://www.dabeaz.com/per.html) 以及 
[ Python Cookbook (O'Reilly Media)](http://www.dabeaz.com/cookbook.html) 的作者。

David Beazley 大神的博客地址：<http://www.dabeaz.com/>

## 译者的话

人生苦短，我用 Python！

译者一直坚持使用 Python 3，因为它代表了 Python 的未来。虽然向后兼容是它的硬伤，但是这个局面迟早会改变的，
而且 Python 3 的未来需要每个人的帮助和支持。
目前市面上的教程书籍，网上的手册大部分基本都是 2.x 系列的，专门基于 3.x 系列的书籍少得可怜。

最近看到一本 _Python Cookbook_ 3rd Edition，完全基于 Python 3，写的也很不错。
为了 Python 3 的普及，我也不自量力，想做点什么事情。于是乎，就有了翻译这本书的冲动了！
这不是一项轻松的工作，却是一件值得做的工作：不仅方便了别人，而且对自己的翻译能力也是一种锻炼和提升。

译者会坚持对自己每一句的翻译负责，力求高质量。但受能力限制，也难免有疏漏或者表意不当的地方。
如果译文中有什么错漏的地方请大家见谅，也欢迎大家随时指正。

目前已经正式完成了整本书的翻译工作，历时2年，不管怎样还是坚持下来了。现在共享给 Python 社区。

**欢迎关注我的个人公众号“飞污熊”，我会定期分享一些自己的 Python 学习笔记和心得。**

![公众号](https://github.com/yidao620c/python3-cookbook/raw/master/exts/wuxiong.jpg)


## 项目说明

* 所有文档均使用 reStructuredText 编辑，参考 [reStructuredText](http://docutils.sourceforge.net/docs/user/rst/quickref.html)
* 当前文档生成托管在 [Read the Docs](https://readthedocs.org/) 上
* 生成的文档预览地址： [python3-cookbook](http://python3-cookbook.readthedocs.org/zh_CN/latest/)
* 使用了 Python 官方文档主题 [sphinx-rtd-theme](https://github.com/snide/sphinx_rtd_theme)，也是默认的主题
* 书中所有代码均在 Python 3.6 版本下运行通过，所有源码放在 cookbook 包下面

```
# on_rtd is whether we are on readthedocs.org, this line of code grabbed from docs.readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# otherwise, readthedocs.org uses their theme by default, so no need to specify it
```

## 其他贡献者

排名不分先后：

1. Yu Longjun (https://github.com/yulongjun)
1. tylinux (https://github.com/tylinux)
1. Kevin Guan (https://github.com/K-Guan)
1. littlezz (https://github.com/littlezz)
1. cclauss (https://github.com/cclauss)
1. Yan Zhang (https://github.com/Eskibear)
1. xiuyanduan (https://github.com/xiuyanduan)
1. FPlust (https://github.com/fplust)
1. lambdaplus (https://github.com/lambdaplus)
1. Tony Yang (liuliu036@gmail.com)

[更多贡献者](https://github.com/yidao620c/python3-cookbook/graphs/contributors)

-----------------------------------------------------

## 关于源码生成 PDF 文件

有网友提问怎样通过源码生成 PDF 文件，由于这个步骤介绍有点长，不适合放在 README 中，我专门写了篇博客专门介绍怎样通过 Read the Docs 托管文档，怎样自己生成 PDF 文件，大家可以参考一下。

<https://www.xncoding.com/2017/01/22/fullstack/readthedoc.html>

另外关于生成的 PDF 文件中会自动生成标题编号的问题，有热心网友 [CarlKing5019](https://github.com/CarlKing5019) 提出了解决方案，
请参考 [issues#108](https://github.com/yidao620c/python3-cookbook/issues/108)。

再次感谢每一位贡献者。

-----------------------------------------------------

## How to Contribute

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

## License

(The Apache License)

Copyright (c) 2014-2018 [Xiong Neng](<https://www.xncoding.com/>) and other contributors

Licensed under the Apache License, Version 2.0 (the "License"); 
you may not use this file except in compliance with the License. You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, 
software distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
See the License for the specific language governing permissions and limitations under the License.


[licensesvg]: https://img.shields.io/hexpm/l/plug.svg
[license]: http://www.apache.org/licenses/LICENSE-2.0
