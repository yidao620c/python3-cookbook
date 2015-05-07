==============================
13.9 通过文件名查找文件
==============================

----------
问题
----------
You need to write a script that involves finding files, like a file renaming script or a log
archiver utility, but you’d rather not have to call shell utilities from within your Python
script, or you want to provide specialized behavior not easily available by “shelling out.”

|

----------
解决方案
----------
To search for files, use the os.walk() function, supplying it with the top-level directory.
Here is an example of a function that finds a specific filename and prints out the full
path of all matches:

#!/usr/bin/env python3.3
import os

def findfile(start, name):
    for relpath, dirs, files in os.walk(start):
        if name in files:
            full_path = os.path.join(start, relpath, name)
            print(os.path.normpath(os.path.abspath(full_path)))

if __name__ == '__main__':
    findfile(sys.argv[1], sys.argv[2])

Save this script as findfile.py and run it from the command line, feeding in the starting
point and the name as positional arguments, like this:

bash % ./findfile.py . myfile.txt

|

----------
讨论
----------
The os.walk() method traverses the directory hierarchy for us, and for each directory
it enters, it returns a 3-tuple, containing the relative path to the directory it’s inspecting,
a list containing all of the directory names in that directory, and a list of filenames in
that directory.
For each tuple, you simply check if the target filename is in the  files list. If it is,
os.path.join() is used to put together a path. To avoid the possibility of weird looking
paths like ././foo//bar, two additional functions are used to fix the result. The first is
os.path.abspath(), which takes a path that might be relative and forms the absolute
path, and the second is os.path.normpath(), which will normalize the path, thereby
resolving issues with double slashes, multiple references to the current directory, and 
so on.
Although this script is pretty simple compared to the features of the find utility found
on UNIX platforms, it has the benefit of being cross-platform. Furthermore, a lot of
additional functionality can be added in a portable manner without much more work.
To illustrate, here is a function that prints out all of the files that have a recent modifi‐
cation time:

#!/usr/bin/env python3.3

import os
import time

def modified_within(top, seconds):
    now = time.time()
    for path, dirs, files in os.walk(top):
        for name in files:
            fullpath = os.path.join(path, name)
            if os.path.exists(fullpath):
                mtime = os.path.getmtime(fullpath)
                if mtime > (now - seconds):
                    print(fullpath)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('Usage: {} dir seconds'.format(sys.argv[0]))
        raise SystemExit(1)

    modified_within(sys.argv[1], float(sys.argv[2]))

It wouldn’t take long for you to build far more complex operations on top of this little
function using various features of the os, os.path, glob, and similar modules. See Rec‐
ipes 5.11 and 5.13 for related recipes.
