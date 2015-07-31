=============================
第十五章：C语言扩展
=============================

本章着眼于从Python访问C代码的问题。许多Python内置库是用C写的，访问C是让Python的对现有库进行交互一个重要的组成部分。这也是一个当你面临从Python 2 到 Python 3扩展代码的问题。虽然Python提供了一个广泛的编程API，实际上有很多方法来处理C的代码。相比试图给出对于每一个可能的工具或技术的详细参考，我么采用的是是集中在一个小片段的C++代码，以及一些有代表性的例子来展示如何与代码交互。这个目标是提供一系列的编程模板，有经验的程序员可以扩展自己的使用。

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

This code contains a number of different C programming features. First, there are a few
simple functions such as gcd() and is_mandel(). The divide() function is an example
of a C function returning multiple values, one through a pointer argument. The avg()
function performs a data reduction across a C array. The Point and distance() function
involve C structures.


For all of the recipes that follow, assume that the preceding code is found in a file named
sample.c, that definitions are found in a file named sample.h and that it has been compiled
into a library libsample that can be linked to other C code. The exact details of
compilation and linking vary from system to system, but that is not the primary focus.
It is assumed that if you’re working with C code, you’ve already figured that out.


Contents:

.. toctree::
   :maxdepth: 1
   :glob:

   ../c15/*
