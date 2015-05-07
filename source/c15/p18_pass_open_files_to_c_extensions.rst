==============================
15.18 传递已打开的文件给C扩展
==============================

----------
问题
----------
You have an open file object in Python, but need to pass it to C extension code that will
use the file.

Solution
To convert a file to an integer file descriptor, use PyFile_FromFd(), as shown:

PyObject *fobj;     /* File object (already obtained somehow) */
int fd = PyObject_AsFileDescriptor(fobj);
if (fd < 0) {
   return NULL;
}

The resulting file descriptor is obtained by calling the fileno() method on fobj. Thus,
any object that exposes a descriptor in this manner should work (e.g., file, socket, etc.).
Once you have the descriptor, it can be passed to various low-level C functions that
expect to work with files.
If  you  need  to  convert  an  integer  file  descriptor  back  into  a  Python  object,  use
PyFile_FromFd() as follows:

int fd;     /* Existing file descriptor (already open) */
PyObject *fobj = PyFile_FromFd(fd, "filename","r",-1,NULL,NULL,NULL,1);

The arguments to PyFile_FromFd() mirror those of the built-in open() function. NULL
values simply indicate that the default settings for the encoding, errors, and newline
arguments are being used.

Discussion
If you are passing file objects from Python to C, there are a few tricky issues to be
concerned about. First, Python performs its own I/O buffering through the io module.
Prior to passing any kind of file descriptor to C, you should first flush the I/O buffers
on the associated file objects. Otherwise, you could get data appearing out of order on
the file stream.
Second, you need to pay careful attention to file ownership and the responsibility of
closing the file in particular. If a file descriptor is passed to C, but still used in Python,
you need to make sure C doesn’t accidentally close the file. Likewise, if a file descriptor
is being turned into a Python file object, you need to be clear about who is responsible
for closing it. The last argument to PyFile_FromFd() is set to 1 to indicate that Python
should close the file.
If you need to make a different kind of file object such as a FILE * object from the C
standard I/O library using a function such as fdopen(), you’ll need to be especially
careful. Doing so would introduce two completely different I/O buffering layers into
the I/O stack (one from Python’s io module and one from C stdio). Operations such
as fclose() in C could also inadvertently close the file for further use in Python. If given
a choice, you should probably make extension code work with the low-level integer file
descriptors as opposed to using a higher-level abstraction such as that provided by
<stdio.h>.
