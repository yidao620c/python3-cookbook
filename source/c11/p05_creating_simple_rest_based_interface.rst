===============================
11.5 生成一个简单的REST接口
===============================

----------
问题
----------
You want to be able to control or interact with your program remotely over the network
using a simple REST-based interface. However, you don’t want to do it by installing a
full-fledged web programming framework.

Solution
One of the easiest ways to build REST-based interfaces is to create a tiny library based
on the WSGI standard, as described in PEP 3333. Here is an example:

# resty.py

import cgi

def notfound_404(environ, start_response):
    start_response('404 Not Found', [ ('Content-type', 'text/plain') ])
    return [b'Not Found']

class PathDispatcher:
    def __init__(self):
        self.pathmap = { }

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        params = cgi.FieldStorage(environ['wsgi.input'],
                                  environ=environ)
        method = environ['REQUEST_METHOD'].lower()
        environ['params'] = { key: params.getvalue(key) for key in params }
        handler = self.pathmap.get((method,path), notfound_404)
        return handler(environ, start_response)

    def register(self, method, path, function):
        self.pathmap[method.lower(), path] = function
        return function

To use this dispatcher, you simply write different handlers, such as the following:

import time

_hello_resp = '''\
<html>
  <head>
     <title>Hello {name}</title>
   </head>
   <body>
     <h1>Hello {name}!</h1>
   </body>
</html>'''

def hello_world(environ, start_response):
    start_response('200 OK', [ ('Content-type','text/html')])
    params = environ['params']
    resp = _hello_resp.format(name=params.get('name'))
    yield resp.encode('utf-8')

_localtime_resp = '''\
<?xml version="1.0"?>
<time>
  <year>{t.tm_year}</year>
  <month>{t.tm_mon}</month>
  <day>{t.tm_mday}</day>
  <hour>{t.tm_hour}</hour>
  <minute>{t.tm_min}</minute>
  <second>{t.tm_sec}</second>
</time>'''

def localtime(environ, start_response):
    start_response('200 OK', [ ('Content-type', 'application/xml') ])
    resp = _localtime_resp.format(t=time.localtime())
    yield resp.encode('utf-8')

if __name__ == '__main__':
    from resty import PathDispatcher
    from wsgiref.simple_server import make_server

    # Create the dispatcher and register functions
    dispatcher = PathDispatcher()
    dispatcher.register('GET', '/hello', hello_world)
    dispatcher.register('GET', '/localtime', localtime)

    # Launch a basic server
    httpd = make_server('', 8080, dispatcher)
    print('Serving on port 8080...')
    httpd.serve_forever()

To test your server, you can interact with it using a browser or urllib. For example:

>>> u = urlopen('http://localhost:8080/hello?name=Guido')
>>> print(u.read().decode('utf-8'))
<html>
  <head>
     <title>Hello Guido</title>
   </head>
   <body>
     <h1>Hello Guido!</h1>
   </body>
</html>
>>> u = urlopen('http://localhost:8080/localtime')
>>> print(u.read().decode('utf-8'))
<?xml version="1.0"?>
<time>

  <year>2012</year>
  <month>11</month>
  <day>24</day>
  <hour>14</hour>
  <minute>49</minute>
  <second>17</second>
</time>
>>>

Discussion
In REST-based interfaces, you are typically writing programs that respond to common
HTTP requests. However, unlike a full-fledged website, you’re often just pushing data
around. This data might be encoded in a variety of standard formats such as XML, JSON,
or CSV. Although it seems minimal, providing an API in this manner can be a very
useful thing for a wide variety of applications.
For example, long-running programs might use a REST API to implement monitoring
or diagnostics. Big data applications can use REST to build a query/data extraction
system. REST can even be used to control hardware devices, such as robots, sensors,
mills, or lightbulbs. What’s more, REST APIs are well supported by various client-side
programming environments, such as Javascript, Android, iOS, and so forth. Thus, hav‐
ing such an interface can be a way to encourage the development of more complex
applications that interface with your code.
For implementing a simple REST interface, it is often easy enough to base your code on
the Python WSGI standard. WSGI is supported by the standard library, but also by most
third-party web frameworks. Thus, if you use it, there is a lot of flexibility in how your
code might be used later.
In WSGI, you simply implement applications in the form of a callable that accepts this
calling convention:

import cgi

def wsgi_app(environ, start_response):
    ...

The environ argument is a dictionary that contains values inspired by the CGI interface
provided by various web servers such as Apache [see Internet RFC 3875]. To extract
different fields, you would write code like this:

def wsgi_app(environ, start_response):
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']
    # Parse the query parameters
    params = cgi.FieldStorage(environ['wsgi.input'], environ=environ)
    ...

A few common values are shown here. environ['REQUEST_METHOD'] is the type of re‐
quest (e.g., GET, POST, HEAD, etc.). environ['PATH_INFO'] is the path or the resource
being requested. The call to cgi.FieldStorage() extracts supplied query parameters
from the request and puts them into a dictionary-like object for later use.
The start_response argument is a function that must be called to initiate a response.
The first argument is the resulting HTTP status. The second argument is a list of (name,
value) tuples that make up the HTTP headers of the response. For example:

def wsgi_app(environ, start_response):
    ...
    start_response('200 OK', [('Content-type', 'text/plain')])

To return data, an WSGI application must return a sequence of byte strings. This can
be done using a list like this:

def wsgi_app(environ, start_response):
    ...
    start_response('200 OK', [('Content-type', 'text/plain')])
    resp = []
    resp.append(b'Hello World\n')
    resp.append(b'Goodbye!\n')
    return resp

Alternatively, you can use yield:

def wsgi_app(environ, start_response):
    ...
    start_response('200 OK', [('Content-type', 'text/plain')])
    yield b'Hello World\n'
    yield b'Goodbye!\n'

It’s important to emphasize that byte strings must be used in the result. If the response
consists of text, it will need to be encoded into bytes first. Of course, there is no re‐
quirement that the returned value be text—you could easily write an application func‐
tion that creates images.
Although WSGI applications are commonly defined as a function, as shown, an instance
may also be used as long as it implements a suitable __call__() method. For example:

class WSGIApplication:
    def __init__(self):
        ...
    def __call__(self, environ, start_response)
       ...

This technique has been used to create the PathDispatcher class in the recipe. The
dispatcher does nothing more than manage a dictionary mapping (method, path) pairs
to handler functions. When a request arrives, the method and path are extracted and
used to dispatch to a handler. In addition, any query variables are parsed and put into

a dictionary that is stored as environ['params'] (this latter step is so common, it makes
a lot of sense to simply do it in the dispatcher in order to avoid a lot of replicated code).
To use the dispatcher, you simply create an instance and register various WSGI-style
application functions with it, as shown in the recipe. Writing these functions should be
extremely straightforward, as you follow the rules concerning the start_response()
function and produce output as byte strings.
One thing to consider when writing such functions is the careful use of string templates.
Nobody likes to work with code that is a tangled mess of print() functions, XML, and
various formatting operations. In the solution, triple-quoted string templates are being
defined and used internally. This particular approach makes it easier to change the
format of the output later (just change the template as opposed to any of the code that
uses it).
Finally, an important part of using WSGI is that nothing in the implementation is spe‐
cific to a particular web server. That is actually the whole idea—since the standard is
server and framework neutral, you should be able to plug your application into a wide
variety of servers. In the recipe, the following code is used for testing:

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    # Create the dispatcher and register functions
    dispatcher = PathDispatcher()
    ...

    # Launch a basic server
    httpd = make_server('', 8080, dispatcher)
    print('Serving on port 8080...')
    httpd.serve_forever()

This will create a simple server that you can use to see if your implementation works.
Later on, when you’re ready to scale things up to a larger level, you will change this code
to work with a particular server.
WSGI is an intentionally minimal specification. As such, it doesn’t provide any support
for more advanced concepts such as authentication, cookies, redirection, and so forth.
These are not hard to implement yourself. However, if you want just a bit more support,
you might consider third-party libraries, such as WebOb or Paste. 

