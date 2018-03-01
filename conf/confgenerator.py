# -*- coding:utf-8 -*-

# conf文件的编辑只能由程序进行，因此先编写一个生成程序
import configparser

"""
生成的conf文件1：/conf/dir.conf
[filepath]
dict = out/dicts.dat
alltext = out/txts.dat
alltextwords = out/txtwords.dat

[filedata]
texttotal = 0


生成的conf文件2：/conf/par.conf
[para]
K = 2
alpha = 0.2
beta = 0.2
iters = 3

"""

if __name__ == '__main__':
    c1 = configparser.ConfigParser()
    c1['filepath'] = {
        'dict':'output/dicts.dat',
        'alltext':'output/txts.dat',
        'alltextwords':'output/txtwords.dat'
    }
    c1['filedata'] = {
        'texttotal':'0'
    }
    with open('dir.conf','w') as c1wt:
        c1.write(c1wt)

    c2 = configparser.ConfigParser()
    c2['para'] = {
        'K':'5',
        'alpha':'0.1',
        'beta':'0.1',
        'iters':'100'
    }
    with open('par.conf','w') as c2wt :
        c2.write(c2wt)

    # 输出测试
    # c3 = configparser.ConfigParser()
    # c3.read('par.conf')
    # print(c3.get('para','alpha'))
    fileconf = configparser.ConfigParser()
    fileconf.read("dir.conf")
    print(fileconf.get("filepath", "alltext"))
