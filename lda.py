# -*- coding:utf-8 -*-
import random

import numpy as np

import doc_processing
from settings import Configs

class LDAModel(object):

    def __init__(self):
        # 从para.conf中读取参数
        pc = Configs()
        pc.confgetparas()
        self.K = pc.K
        self.alpha = pc.alpha
        self.beta = pc.beta
        self.iter_times = pc.iters
        # self.top_words_num = top_words_num 每个类特征词个数
        print('paras: K='+str(self.K)+' alpha='+str(self.alpha)+' beta='+str(self.beta)+' iter='+str(self.iter_times))

        # 从dir.conf中读取文档路径
        dc = Configs()
        dc.confgetpaths()
        # 打开文档读取到变量
        alltfr = open(dc.alltextfile,'r',encoding='utf8')
        self.all_text = []  # 存储每个文档的所有词语列表[ ['a','b','c'],[...],...]
        for lines in alltfr.readlines():
            strs = lines.replace('\n', '')
            wordlist = strs.split(' ')
            self.all_text.append(wordlist)
        print(self.all_text)
        alltfr.close()

        alltwfr = open(dc.alltextwordsfile,'r',encoding='utf8')
        self.all_text_words = []    # 存储每篇文档词数
        for lines in alltwfr.readlines():
            self.all_text_words.append(lines.replace('\n',''))
        print(self.all_text_words)
        alltwfr.close()

        dictfr = open(dc.dictfile,'r',encoding='utf8')
        self.dicts = []
        for lines in dictfr.readlines():
            self.dicts.append(lines.replace('\n',''))
        print(self.dicts)
        dictfr.close()

        self.V = len(self.dicts)
        self.M = len(self.all_text)

        self.p = np.zeros(self.K)   # 每次gibbs sampling的临时变量
        self.nw = np.zeros((self.V,self.K),dtype=np.int)
        self.nwsum = np.zeros(self.K, dtype=np.int)
        self.nd = np.zeros((self.M,self.K),dtype=np.int)
        self.ndsum = np.zeros(self.M,dtype=np.int)
        self.Z = []
        for i in range(0,self.M):
            self.Z.append(np.zeros(int(self.all_text_words[i]),dtype=np.int))
        # self.Z = np.zeros(self.textlen,每篇词数)

        self.theta = np.zeros((self.M,self.K),dtype=np.float)
        self.phi = np.zeros((self.K,self.V),dtype=np.float)


        # 随机分配类型
        for m in range(0, self.M):
            self.ndsum[m] = int(self.all_text_words[m])
            for y in range(0,int(self.all_text_words[m])):
                topic = random.randint(0,self.K-1)  # topic编号应该从1到K
                self.Z[m][y] = topic
                self.nw[self.dicts.index(self.all_text[m][y])][topic] += 1   # 词典，顺序必须和nw的V*K维对应，中间不能有变化
                self.nd[m][topic] += 1
                self.nwsum[topic] += 1
        print('随机分配结果：')
        print(self.Z)

    # 核心：sampling函数
    def sampling(self,i,j):
        topic = self.Z[i][j]
        word = self.all_text[i][j]
        self.nw[self.dicts.index(word)][topic] -= 1
        self.nd[i][topic] -= 1
        self.nwsum[topic] -= 1
        self.ndsum[i] -= 1
        Kalpha = self.K * self.alpha
        Vbeta = self.V * self.beta
        self.p = (self.nw[self.dicts.index(word)] + self.beta) / (self.nwsum + Vbeta) * \
                 (self.nd[i] + self.alpha) / (self.ndsum[i] + Kalpha)

        for k in range(0,self.K):
            self.p[k] += self.p[k-1]
        u = random.uniform(0,self.p[self.K-1])
        for topic in range(0,self.K):
            if self.p[topic]>u:
                break

        self.nw[self.dicts.index(word)][topic] += 1
        self.nwsum[topic] += 1
        self.nd[i][topic] += 1
        self.ndsum[i] += 1

        return topic


    # 循环每个词调用sampling函数
    def start(self):
        for itr in range(0,self.iter_times):
            for m in range(0,self.M):
                for w in range(0,int(self.all_text_words[m])):
                    topic = self.sampling(m,w)
                    self.Z[m][w] = topic
        # logging
        print(self.Z)



    # 评价方法
    # 误报率 = 错分到某类的/（错分+正分到此类的）
    # 漏报率 = （此类本来的-正分到此类的）/此类本来的
    # F值
    # 毕设的短文本相似度分析还是不用这个评价方法了...
    # 项目中只分两类或三类是比较方便的

def run():
    [all_text_num, all_dict_len]= doc_processing.doc_process()  # 讲道理也可以把所有文件信息通过传参传进来
    lda = LDAModel()#all_text_num,all_dict_len)
    lda.start()


if __name__ == '__main__':
    run()
