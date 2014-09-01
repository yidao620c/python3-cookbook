# encoding: utf-8
"""
    Topic: sample
    Desc:  
"""
import os
__author__ = 'Xiong Neng'


def main():
    for tmpdir in ('/tmp', r'c:\temp'):
        if os.path.isdir(tmpdir):
            print('find tmpdir:', tmpdir)
            break
    else:
        print('no temp dir available')
        tempdir = ''

    if tmpdir:
        os.chdir(tmpdir)
        cwd = os.getcwd()
        print('*** current temporary directory:')
        print(cwd)

        print('-------')
        os.mkdir('example')
        os.chdir('example')
        cwd = os.getcwd()
        print('now...', cwd)
        print('list dir:', os.listdir(cwd))

        print('----create test file-----')
        fobj = open('test.txt', 'w')
        fobj.write('this is a line....\n')
        fobj.write('second line....\n')
        fobj.close()
        print('--------now again list...-------')
        print(os.listdir(cwd))

        print('----------rename----------')
        os.rename('test.txt', 'new_test.txt')
        print('----------after rename-------')
        print(os.listdir(cwd))

        path = os.path.join(cwd, os.listdir(cwd)[0])
        print('join,,,,full file path is :', path)
        print('---(filepath, basename)---', os.path.split(path))
        print('====(filename, extension====', os.path.splitext(os.path.basename(path)))

        print('-----display file contents----')
        fobj = open(path)
        for eachline in fobj:
            print(eachline),
        fobj.close()

        print('-----------delete test file---------')
        os.remove(path)
        print('-----------udpated directory listing:----')
        print(os.listdir(cwd))
        os.chdir(os.pardir)
        print('------after change dir to the parent dir------')
        print('now list dirs:', os.listdir(os.getcwd()))
        print('-------delete test directory---------')
        os.rmdir('example')
        print('now list dirs:', os.listdir(os.getcwd()))
        print('=========================END======================')


if __name__ == '__main__':
    main()
