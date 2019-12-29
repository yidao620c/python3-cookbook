=============================
第一章：数据结构和算法
=============================

Python 提供了大量的内置数据结构，包括列表，集合以及字典。大多数情况下使用这些数据结构是很简单的。
但是，我们也会经常碰到到诸如查询，排序和过滤等等这些普遍存在的问题。
因此，这一章的目的就是讨论这些比较常见的问题和算法。
另外，我们也会给出在集合模块 ``collections`` 当中操作这些数据结构的方法。




.. toctree::
   :maxdepth: 1
   :glob:

   ../c01/*

=============================
第二章：字符串和文本
=============================

几乎所有有用的程序都会涉及到某些文本处理，不管是解析数据还是产生输出。
这一章将重点关注文本的操作处理，比如提取字符串，搜索，替换以及解析等。
大部分的问题都能简单的调用字符串的内建方法完成。
但是，一些更为复杂的操作可能需要正则表达式或者强大的解析器，所有这些主题我们都会详细讲解。
并且在操作Unicode时候碰到的一些棘手的问题在这里也会被提及到。


Contents:

.. toctree::
   :maxdepth: 1
   :glob:

   ../c02/*

=============================
第三章：数字日期和时间
=============================

在Python中执行整数和浮点数的数学运算时很简单的。
尽管如此，如果你需要执行分数、数组或者是日期和时间的运算的话，就得做更多的工作了。
本章集中讨论的就是这些主题。


Contents:

.. toctree::
   :maxdepth: 1
   :glob:

   ../c03/*

=============================
第四章：迭代器与生成器
=============================

迭代是Python最强大的功能之一。初看起来，你可能会简单的认为迭代只不过是处理序列中元素的一种方法。
然而，绝非仅仅就是如此，还有很多你可能不知道的，
比如创建你自己的迭代器对象，在itertools模块中使用有用的迭代模式，构造生成器函数等等。
这一章目的就是向你展示跟迭代有关的各种常见问题。


Contents:

.. toctree::
   :maxdepth: 1
   :glob:

   ../c04/*

=============================
第五章：文件与IO
=============================

所有程序都要处理输入和输出。
这一章将涵盖处理不同类型的文件，包括文本和二进制文件，文件编码和其他相关的内容。
对文件名和目录的操作也会涉及到。

Contents:

.. toctree::
   :maxdepth: 1
   :glob:

   ../c05/*

=============================
第六章：数据编码和处理
=============================

这一章主要讨论使用Python处理各种不同方式编码的数据，比如CSV文件，JSON，XML和二进制包装记录。
和数据结构那一章不同的是，这章不会讨论特殊的算法问题，而是关注于怎样获取和存储这些格式的数据。


Contents:

.. toctree::
   :maxdepth: 1
   :glob:

   ../c06/*

=============================
第七章：函数
=============================

使用 ``def`` 语句定义函数是所有程序的基础。
本章的目标是讲解一些更加高级和不常见的函数定义与使用模式。
涉及到的内容包括默认参数、任意数量参数、强制关键字参数、注解和闭包。
另外，一些高级的控制流和利用回调函数传递数据的技术在这里也会讲解到。


Contents:

.. toctree::
   :maxdepth: 1
   :glob:

   ../c07/*

=============================
第八章：类与对象
=============================

本章主要关注点的是和类定义有关的常见编程模型。包括让对象支持常见的Python特性、特殊方法的使用、
类封装技术、继承、内存管理以及有用的设计模式。


Contents:

.. toctree::
   :maxdepth: 1
   :glob:

   ../c08/*

=============================
第九章：元编程
=============================

软件开发领域中最经典的口头禅就是“don’t repeat yourself”。
也就是说，任何时候当你的程序中存在高度重复(或者是通过剪切复制)的代码时，都应该想想是否有更好的解决方案。
在Python当中，通常都可以通过元编程来解决这类问题。
简而言之，元编程就是关于创建操作源代码(比如修改、生成或包装原来的代码)的函数和类。
主要技术是使用装饰器、类装饰器和元类。不过还有一些其他技术，
包括签名对象、使用 ``exec()`` 执行代码以及对内部函数和类的反射技术等。
本章的主要目的是向大家介绍这些元编程技术，并且给出实例来演示它们是怎样定制化你的源代码行为的。


Contents:

.. toctree::
   :maxdepth: 1
   :glob:

   ../c09/*

=============================
第十章：模块与包
=============================

模块与包是任何大型程序的核心，就连Python安装程序本身也是一个包。本章重点涉及有关模块和包的常用编程技术，例如如何组织包、把大型模块分割成多个文件、创建命名空间包。同时，也给出了让你自定义导入语句的秘籍。


Contents:

.. toctree::
   :maxdepth: 1
   :glob:

   ../c10/*

=============================
第十一章：网络与Web编程
=============================

本章是关于在网络应用和分布式应用中使用的各种主题。主题划分为使用Python编写客户端程序来访问已有的服务，以及使用Python实现网络服务端程序。也给出了一些常见的技术，用于编写涉及协同或通信的的代码。

Contents:

.. toctree::
   :maxdepth: 1
   :glob:

   ../c11/*

=============================
第十二章：并发编程
=============================

对于并发编程, Python有多种长期支持的方法, 包括多线程, 调用子进程, 以及各种各样的关于生成器函数的技巧.
这一章将会给出并发编程各种方面的技巧, 包括通用的多线程技术以及并行计算的实现方法.

像经验丰富的程序员所知道的那样, 大家担心并发的程序有潜在的危险.
因此, 本章的主要目标之一是给出更加可信赖和易调试的代码.

Contents:

.. toctree::
   :maxdepth: 1
   :glob:

   ../c12/*

=============================
第十三章：脚本编程与系统管理
=============================

许多人使用Python作为一个shell脚本的替代，用来实现常用系统任务的自动化，如文件的操作，系统的配置等。本章的主要目标是描述关于编写脚本时候经常遇到的一些功能。例如，解析命令行选项、获取有用的系统配置数据等等。第5章也包含了与文件和目录相关的一般信息。

Contents:

.. toctree::
   :maxdepth: 1
   :glob:

   ../c13/*

=============================
第十四章：测试、调试和异常
=============================

试验还是很棒的，但是调试？就没那么有趣了。事实是，在Python测试代码之前没有编译器来分析你的代码，因此使得测试成为开发的一个重要部分。本章的目标是讨论一些关于测试、调试和异常处理的常见问题。但是并不是为测试驱动开发或者单元测试模块做一个简要的介绍。因此，笔者假定读者熟悉测试概念。


Contents:

.. toctree::
   :maxdepth: 1
   :glob:

   ../c14/*

=============================
第十五章：C语言扩展
=============================

本章着眼于从Python访问C代码的问题。许多Python内置库是用C写的，
访问C是让Python的对现有库进行交互一个重要的组成部分。
这也是一个当你面临从Python 2 到 Python 3扩展代码的问题。
虽然Python提供了一个广泛的编程API，实际上有很多方法来处理C的代码。
相比试图给出对于每一个可能的工具或技术的详细参考，
我们采用的是是集中在一个小片段的C++代码，以及一些有代表性的例子来展示如何与代码交互。
这个目标是提供一系列的编程模板，有经验的程序员可以扩展自己的使用。

这里是我们将在大部分秘籍中工作的代码：

.. code-block:: c

    /* sample.c */_method
    #include <math.h>

    /* Compute the greatest common divisor */
    int gcd(int x, int y) {
        int g = y;
        while (x > 0) {
            g = x;
            x = y % x;
            y = g;
        }
        return g;
    }

    /* Test if (x0,y0) is in the Mandelbrot set or not */
    int in_mandel(double x0, double y0, int n) {
        double x=0,y=0,xtemp;
        while (n > 0) {
            xtemp = x*x - y*y + x0;
            y = 2*x*y + y0;
            x = xtemp;
            n -= 1;
            if (x*x + y*y > 4) return 0;
        }
        return 1;
    }

    /* Divide two numbers */
    int divide(int a, int b, int *remainder) {
        int quot = a / b;
        *remainder = a % b;
        return quot;
    }

    /* Average values in an array */
    double avg(double *a, int n) {
        int i;
        double total = 0.0;
        for (i = 0; i < n; i++) {
            total += a[i];
        }
        return total / n;
    }

    /* A C data structure */
    typedef struct Point {
        double x,y;
    } Point;

    /* Function involving a C data structure */
    double distance(Point *p1, Point *p2) {
        return hypot(p1->x - p2->x, p1->y - p2->y);
    }

这段代码包含了多种不同的C语言编程特性。
首先，这里有很多函数比如 ``gcd()`` 和 ``is_mandel()`` 。
``divide()`` 函数是一个返回多个值的C函数例子，其中有一个是通过指针参数的方式。
``avg()`` 函数通过一个C数组执行数据聚集操作。``Point`` 和 ``distance()`` 函数涉及到了C结构体。

对于接下来的所有小节，先假定上面的代码已经被写入了一个名叫“sample.c”的文件中，
然后它们的定义被写入一个名叫“sample.h”的头文件中，
并且被编译为一个库叫“libsample”，能被链接到其他C语言代码中。
编译和链接的细节依据系统的不同而不同，但是这个不是我们关注的。
如果你要处理C代码，我们假定这些基础的东西你都掌握了。

Contents:

.. toctree::
   :maxdepth: 1
   :glob:

   ../c15/*

=============================
附录A
=============================

-------------------
在线资源
-------------------
http://docs.python.org
   
如果你需要深入了解探究语言和模块的细节，那么不必说，Python自家的在线文档是一个卓越的资源。只要保证你查看的是python 3 的文档而不是以前的老版本
  
http://www.python.org/dev/peps
   
如果你向理解为python语言添加新特性的动机以及实现的细节，那么PEPs（Python Enhancement Proposals----Python开发编码规范）绝对是非常宝贵的资源。尤其是一些高级语言功能更是如此。在写这本书的时候，PEPS通常比官方文档管用。

http://pyvideo.org

这里有来自最近的PyCon大会、用户组见面会等的大量视频演讲和教程素材。对于学习潮流的python开发是非常宝贵的资源。许多视频中都会有Python的核心开发者现身说法，讲解Python 3中添加的的新特性。
   
http://code.activestate.com/recipes/langs/python
   
长期以来，ActiveState的Python版块已经成为一个找到数以千计的针对特定编程问题的解决方案。到写作此书位置，已经包含了大约300个特定于Python3的秘籍。你会发现，其中多数的秘籍要么对本书覆盖的话题进行了扩展，要么专精于具体的任务。所以说，它是一个好伴侣。
   
http://stackoverflow.com/questions/tagged/python
   
Stack Overflow 目前有超过175,000个问题被标记为Python相关（而其中大约5000个问题是针对Python 3的）。尽管问题和回答的质量不同，但是仍然能发现很多好优秀的素材。

-------------------
Python学习书籍
-------------------
下面这些书籍提供了对Python编程的入门介绍，且重点放在了Python 3上。

* *Learning Python*，第四版 ，作者 Mark Lutz， O’Reilly & Associates 出版 (2009)。
* *The Quick Python Book*，作者 Vernon Ceder， Manning 出版(2010)。
* *Python Programming for the Absolute Beginner*，第三版，作者 Michael Dawson，Course Technology PTR 出版(2010).
* *Beginning Python: From Novice to Professional*，第二版， 作者 Magnus Lie Het‐ land， Apress 出版(2008).
* *Programming in Python 3*，第二版，作者 Mark Summerfield，Addison-Wesley 出版 (2010).

-------------------
高级书籍
-------------------
下面的这些书籍提供了更多高级的范围，也包含Python 3方面的内容。

* *Programming Python*，第四版, by Mark Lutz, O’Reilly & Associates 出版(2010).
* *Python Essential Reference*，第四版，作者 David Beazley, Addison-Wesley 出版(2009).
* *Core Python Applications Programming*，第三版，作者 Wesley Chun, Prentice Hall 出版(2012).
* *The Python Standard Library by Example* ， 作者 Doug Hellmann，Addison-Wesley 出版(2011).
* *Python 3 Object Oriented Programming*，作者 Dusty Phillips, Packt Publishing 出版(2010).
* *Porting to Python 3*， 作者 Lennart Regebro，CreateSpace 出版(2011), http://python3porting.com.
