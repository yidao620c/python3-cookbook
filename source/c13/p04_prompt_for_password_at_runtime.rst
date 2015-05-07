==============================
13.4 运行时弹出密码输入提示
==============================

----------
问题
----------
You’ve written a script that requires a password, but since the script is meant for inter‐
active use, you’d like to prompt the user for a password rather than hardcode it into the
script.

|

----------
解决方案
----------
Python’s getpass module is precisely what you need in this situation. It will allow you
to very easily prompt for a password without having the keyed-in password displayed
on the user’s terminal. Here’s how it’s done:

import getpass

user = getpass.getuser()
passwd = getpass.getpass()

if svc_login(user, passwd):    # You must write svc_login()
   print('Yay!')
else:
   print('Boo!')

In this code, the svc_login() function is code that you must write to further process
the password entry. Obviously, the exact handling is application-specific.

|

----------
讨论
----------
Note in the preceding code that getpass.getuser() doesn’t prompt the user for their
username. Instead, it uses the current user’s login name, according to the user’s shell
environment, or as a last resort, according to the local system’s password database (on
platforms that support the pwd module).

If you want to explicitly prompt the user for their username, which can be more reliable,
use the built-in input function:

user = input('Enter your username: ')

It’s also important to remember that some systems may not support the hiding of the
typed password input to the getpass() method. In this case, Python does all it can to
forewarn you of problems (i.e., it alerts you that passwords will be shown in cleartext)
before moving on.
