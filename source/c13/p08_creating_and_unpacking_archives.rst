==============================
13.8 创建和解压压缩文件
==============================

----------
问题
----------
You need to create or unpack archives in common formats (e.g., .tar, .tgz, or .zip).

Solution
The shutil module has two functions—make_archive() and unpack_archive()—that
do exactly what you want. For example:

>>> import shutil
>>> shutil.unpack_archive('Python-3.3.0.tgz')

>>> shutil.make_archive('py33','zip','Python-3.3.0')
'/Users/beazley/Downloads/py33.zip'
>>>

The second argument to make_archive() is the desired output format. To get a list of
supported archive formats, use get_archive_formats(). For example:

>>> shutil.get_archive_formats()
[('bztar', "bzip2'ed tar-file"), ('gztar', "gzip'ed tar-file"),
 ('tar', 'uncompressed tar file'), ('zip', 'ZIP file')]
>>>

Discussion
Python has other library modules for dealing with the low-level details of various archive
formats (e.g., tarfile, zipfile, gzip, bz2, etc.). However, if all you’re trying to do is
make or extract an archive, there’s really no need to go so low level. You can just use
these high-level functions in shutil instead.
The functions have a variety of additional options for logging, dryruns, file permissions,
and so forth. Consult the shutil library documentation for further details.
