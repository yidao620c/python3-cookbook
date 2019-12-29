#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 临时文件和目录
Desc : 
"""
from tempfile import TemporaryFile
from tempfile import TemporaryDirectory
from tempfile import NamedTemporaryFile
import tempfile


def temp_file():
    with TemporaryFile('w+t') as f:
        # Read/write to the file
        f.write('Hello World\n')
        f.write('Testing\n')

        # Seek back to beginning and read the data
        f.seek(0)
        data = f.read()
        print(data)

    with NamedTemporaryFile('w+t') as f:
        print('filename is:', f.name)

    with TemporaryDirectory() as dirname:
        print('dirname is:', dirname)

    print(tempfile.mkstemp())
    print(tempfile.mkdtemp())
    print(tempfile.gettempdir())

if __name__ == '__main__':
    temp_file()

