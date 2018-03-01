# -*- coding:utf-8 -*-
# 需要保存的设置分为：
# ---K，alpha等参数          | .conf格式保存
# ---各类文件路径（文件包括）  | .conf保存
# ------词典                | 使用一般文件保存（注意分行）
# ------每条文档内容（分词后） | 使用一般文件保存（注意分行）
# ------每条文档词数         | 一般文件保存
# ------总文档数             | 一般文件保存
# ---日志文件（最后再加上）

#!!! .conf文件只能通过代码运行生成，不能用记事本打开编辑!!!


import configparser
import os

class Configs(object):
    def __init__(self):
        self.alltextfile = ''
        self.dictfile = ''
        self.alltextwordsfile = ''
        self.texttotalnum = 0
        self.K = 3
        self.alpha = 0.1
        self.beta = 0.1
        self.iters = 1

    def confgetpaths(self):
        path = os.getcwd()
        fileconf = configparser.ConfigParser()
        fileconf.read(path+"/conf/dir.conf")
        self.alltextfile = os.path.join(path,os.path.normpath(fileconf.get("filepath", "alltext")))
        self.dictfile = os.path.join(path,os.path.normpath(fileconf.get("filepath", "dict")))
        self.alltextwordsfile = os.path.join(path,os.path.normpath(fileconf.get("filepath", "alltextwords")))
        self.texttotalnum = int(fileconf.get("filedata", "texttotal"))

    def confgetparas(self):
        path = os.getcwd()
        parconf = configparser.ConfigParser()
        parconf.read(path + "/conf/par.conf")
        self.K = int(parconf.get("para", "K"))
        self.alpha = float(parconf.get("para", "alpha"))
        self.beta = float(parconf.get("para", "beta"))
        self.iters = int(parconf.get("para", "iters"))

    def confsettextnums(self,num):  # 记录当前文件集中的文档数量
        path = os.getcwd()
        fileconf = configparser.ConfigParser()
        fileconf.read(path + "/conf/dir.conf")
        fileconf.set('filedata','texttotal',str(num))
        fileconf.write(open(path + "/conf/dir.conf",'w'))