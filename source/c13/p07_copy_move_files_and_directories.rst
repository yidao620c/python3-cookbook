==============================
13.7 复制或者移动文件和目录
==============================

----------
问题
----------
You need to copy or move files and directories around, but you don’t want to do it by
calling out to shell commands.

Solution
The shutil module has portable implementations of functions for copying files and
directories. The usage is extremely straightforward. For example:

import shutil

# Copy src to dst. (cp src dst)
shutil.copy(src, dst)

# Copy files, but preserve metadata (cp -p src dst)
shutil.copy2(src, dst)

# Copy directory tree (cp -R src dst)
shutil.copytree(src, dst)

# Move src to dst (mv src dst)
shutil.move(src, dst)

The arguments to these functions are all strings supplying file or directory names. The
underlying semantics try to emulate that of similar Unix commands, as shown in the
comments.
By default, symbolic links are followed by these commands. For example, if the source
file is a symbolic link, then the destination file will be a copy of the file the link points
to. If you want to copy the symbolic link instead, supply the follow_symlinks keyword
argument like this:

shutil.copy2(src, dst, follow_symlinks=False)

If you want to preserve symbolic links in copied directories, do this:

shutil.copytree(src, dst, symlinks=True)

The copytree() optionally allows you to ignore certain files and directories during the
copy process. To do this, you supply an ignore function that takes a directory name
and filename listing as input, and returns a list of names to ignore as a result. For ex‐
ample:

def ignore_pyc_files(dirname, filenames):
    return [name in filenames if name.endswith('.pyc')]

shutil.copytree(src, dst, ignore=ignore_pyc_files)

Since ignoring filename patterns is common, a utility function ignore_patterns() has
already been provided to do it. For example:

shutil.copytree(src, dst, ignore=shutil.ignore_patterns('*~','*.pyc'))

Discussion
Using  shutil to copy files and directories is mostly straightforward. However, one
caution concerning file metadata is that functions such as copy2() only make a best
effort in preserving this data. Basic information, such as access times, creation times,
and permissions, will always be preserved, but preservation of owners, ACLs, resource
forks, and other extended file metadata may or may not work depending on the un‐
derlying operating system and the user’s own access permissions. You probably wouldn’t
want to use a function like shutil.copytree() to perform system backups.
When working with filenames, make sure you use the functions in  os.path for the
greatest portability (especially if working with both Unix and Windows). For example:

>>> filename = '/Users/guido/programs/spam.py'
>>> import os.path
>>> os.path.basename(filename)
'spam.py'
>>> os.path.dirname(filename)
'/Users/guido/programs'
>>> os.path.split(filename)
('/Users/guido/programs', 'spam.py')
>>> os.path.join('/new/dir', os.path.basename(filename))
'/new/dir/spam.py'
>>> os.path.expanduser('~/guido/programs/spam.py')
'/Users/guido/programs/spam.py'
>>>

One tricky bit about copying directories with copytree() is the handling of errors. For
example, in the process of copying, the function might encounter broken symbolic links,
files that can’t be accessed due to permission problems, and so on. To deal with this, all
exceptions encountered are collected into a list and grouped into a single exception that
gets raised at the end of the operation. Here is how you would handle it:

try:
    shutil.copytree(src, dst)
except shutil.Error as e:
    for src, dst, msg in e.args[0]:
         # src is source name
         # dst is destination name
         # msg is error message from exception
         print(dst, src, msg)

If  you  supply  the  ignore_dangling_symlinks=True  keyword  argument,  then  copy
tree() will ignore dangling symlinks.
The functions shown in this recipe are probably the most commonly used. However,
shutil has many more operations related to copying data. The documentation is def‐
initely worth a further look. See the Python documentation.
