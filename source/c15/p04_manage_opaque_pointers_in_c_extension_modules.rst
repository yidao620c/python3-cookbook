==============================
15.4 在C扩展模块中操作隐形指针
==============================

----------
问题
----------
You have an extension module that needs to handle a pointer to a C data structure, but
you don’t want to expose any internal details of the structure to Python.

|

----------
解决方案
----------
Opaque data structures are easily handled by wrapping them inside capsule objects.
Consider this fragment of C code from our sample code:

typedef struct Point {
    double x,y;
} Point;

extern double distance(Point *p1, Point *p2);

Here is an example of extension code that wraps the Point structure and distance()
function using capsules:

/* Destructor function for points */
static void del_Point(PyObject *obj) {
  free(PyCapsule_GetPointer(obj,"Point"));
}

/* Utility functions */
static Point *PyPoint_AsPoint(PyObject *obj) {
  return (Point *) PyCapsule_GetPointer(obj, "Point");
}

static PyObject *PyPoint_FromPoint(Point *p, int must_free) {
  return PyCapsule_New(p, "Point", must_free ? del_Point : NULL);
}

/* Create a new Point object */
static PyObject *py_Point(PyObject *self, PyObject *args) {

  Point *p;
  double x,y;
  if (!PyArg_ParseTuple(args,"dd",&x,&y)) {
    return NULL;
  }
  p = (Point *) malloc(sizeof(Point));
  p->x = x;
  p->y = y;
  return PyPoint_FromPoint(p, 1);
}

static PyObject *py_distance(PyObject *self, PyObject *args) {
  Point *p1, *p2;
  PyObject *py_p1, *py_p2;
  double result;

  if (!PyArg_ParseTuple(args,"OO",&py_p1, &py_p2)) {
    return NULL;
  }
  if (!(p1 = PyPoint_AsPoint(py_p1))) {
    return NULL;
  }
  if (!(p2 = PyPoint_AsPoint(py_p2))) {
    return NULL;
  }
  result = distance(p1,p2);
  return Py_BuildValue("d", result);
}

Using these functions from Python looks like this:

>>> import sample
>>> p1 = sample.Point(2,3)
>>> p2 = sample.Point(4,5)
>>> p1
<capsule object "Point" at 0x1004ea330>
>>> p2
<capsule object "Point" at 0x1005d1db0>
>>> sample.distance(p1,p2)
2.8284271247461903
>>>

|

----------
讨论
----------
Capsules are similar to a typed C pointer. Internally, they hold a generic pointer along
with an identifying name and can be easily created using the PyCapsule_New() function.
In addition, an optional destructor function can be attached to a capsule to release the
underlying memory when the capsule object is garbage collected.

To extract the pointer contained inside a capsule, use the  PyCapsule_GetPointer()
function and specify the name. If the supplied name doesn’t match that of the capsule
or some other error occurs, an exception is raised and NULL is returned.
In  this  recipe,  a  pair  of  utility  functions—PyPoint_FromPoint()  and  PyPoint_As
Point()—have been written to deal with the mechanics of creating and unwinding
Point instances from capsule objects. In any extension functions, we’ll use these func‐
tions instead of working with capsules directly. This design choice makes it easier to
deal with possible changes to the wrapping of Point objects in the future. For example,
if you decided to use something other than a capsule later, you would only have to change
these two functions.
One tricky part about capsules concerns garbage collection and memory management.
The  PyPoint_FromPoint()  function  accepts  a  must_free  argument  that  indicates
whether the underlying Point * structure is to be collected when the capsule is de‐
stroyed. When working with certain kinds of C code, ownership issues can be difficult
to handle (e.g., perhaps a Point structure is embedded within a larger data structure
that is managed separately). Rather than making a unilateral decision to garbage collect,
this extra argument gives control back to the programmer. It should be noted that the
destructor associated with an existing capsule can also be changed using the  PyCap
sule_SetDestructor() function.
Capsules are a sensible solution to interfacing with certain kinds of C code involving
structures. For instance, sometimes you just don’t care about exposing the internals of
a structure or turning it into a full-fledged extension type. With a capsule, you can put
a lightweight wrapper around it and easily pass it around to other extension functions.
