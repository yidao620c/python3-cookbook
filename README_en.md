
[![GitHub issues](https://img.shields.io/github/issues/yidao620c/python3-cookbook.svg)](https://github.com/yidao620c/python3-cookbook/issues)
[![License][licensesvg]][license]
[![Github downloads](https://img.shields.io/github/downloads/yidao620c/python3-cookbook/total.svg)](https://github.com/yidao620c/python3-cookbook/releases/latest)
[![GitHub release](https://img.shields.io/github/release/yidao620c/python3-cookbook.svg)](https://github.com/yidao620c/python3-cookbook/releases)

Online reading address: http://python3-cookbook.readthedocs.org/zh_CN/latest/

The latest version (3.0.0) download

* Chinese simplified version PDF download address: https://pan.baidu.com/s/1pL1cI9d
* Chinese Traditional Chinese PDF download address: https://pan.baidu.com/s/1qX97VJI

## Translator's words

Life is short, I use Python!

The translator has always insisted on using Python 3 because it represents the future of Python. Although backward compatibility is its flaw, this situation will change sooner or later, and the future of Python3 needs everyone's help and support. At present, the tutorial books on the market, most of the manuals on the Internet are basically 2.x series, and the books based on the 3.x series are less pitiful.

Life is short, I use Python!

The translator has always insisted on using Python 3 because it represents the future of Python. Although backward compatibility is its hard injury, this situation will change sooner or later,
And the future of Python 3 needs everyone's help and support.
At present, the tutorial books on the market, most of the manuals on the Internet are basically 2.x series, and the books based on the 3.x series are less pitiful.

I recently saw a Python Cookbook 3rd Edition, based entirely on Python3, which is also very good.
For the popularity of Python3, I am not self-sufficient and want to do something. Ever since, there is an impulse to translate this book!
This is not an easy job, but it is a worthwhile job: it is not only convenient for others, but also an exercise and improvement for your ability to translate.

The translator will insist on being responsible for the translation of each sentence and strive for high quality. However, due to limited ability, it is inevitable that there will be omissions or improper expressions.
If there is anything wrong with the translation, please forgive me and welcome everyone to correct me.

At present, the translation of the entire book has been officially completed. It lasted for 2 years, and it persisted anyway. Now share it with the python community.

**Welcome to my personal public number "Flying Saffron Bear", I will share some of my own Python study notes and tips on a regular basis. **


[[Public Number] (https://github.com/yidao620c/python3-cookbook/raw/master/exts/wuxiong.jpg)


## project instruction

* All documents are edited using reStructuredText, refer to [reStructuredText] (http://docutils.sourceforge.net/docs/user/rst/quickref.html)
* Current document generation is hosted on [readthedocs] (https://readthedocs.org/)
* Generated document preview address: [python3-cookbook](http://python3-cookbook.readthedocs.org/zh_CN/latest/)
* Use the python official documentation theme [sphinx-rtd-theme] (https://github.com/snide/sphinx_rtd_theme), which is also the default theme default.
* All code in the book runs under Python 3.6, all source code is placed under the cookbook package
```
# on_rtd is whether we are on readthedocs.org, this line of code grabbed from docs.readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# otherwise, readthedocs.org uses their theme by default, so no need to specify it
```

## Other contributors

names not listed in order：

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


[More contributors] (https://github.com/yidao620c/python3-cookbook/graphs/contributors)

-------------------------------------------------- ---

## About source code generation PDF file

Some netizens asked how to generate a PDF file from the source code. Since this step is a bit long, it is not suitable for being placed in the README.
I wrote a blog dedicated to how to use the ReadtheDocs to host documents, how to generate PDF files yourself, you can refer to it.

<https://www.xncoding.com/2017/01/22/fullstack/readthedoc.html>

In addition, the issue of the title number is automatically generated in the generated PDF file, and the enthusiastic user [CarlKing5019] (https://github.com/CarlKing5019) proposes a solution.
Please refer to issues108:

<https://github.com/yidao620c/python3-cookbook/issues/108>

Thanks again to each contributor.

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
