=============================
第十五章：C语言扩展
=============================

This chapter looks at the problem of accessing C code from Python. Many of Python’s
built-in libraries are written in C, and accessing C is an important part of making Python
talk to existing libraries. It’s also an area that might require the most study if you’re faced
with the problem of porting extension code from Python 2 to 3.


Although Python provides an extensive C programming API, there are actually many
different approaches for dealing with C. Rather than trying to give an exhaustive reference
for every possible tool or technique, the approach is to focus on a small fragment
of C code along with some representative examples of how to work with the code. The
goal is to provide a series of programming templates that experienced programmers
can expand upon for their own use.


Here is the C code we will work with in most of the recipes:

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
